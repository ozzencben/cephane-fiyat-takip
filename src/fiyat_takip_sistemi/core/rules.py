import sys
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple
from sqlalchemy import desc
from sqlalchemy.orm import Session

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from .db import SessionLocal
from .models import Competitor, Match, PriceSnapshot, Product


class Severity(str, Enum):
    YUKSEK = "YÜKSEK"
    ORTA = "ORTA"
    DUSUK = "DÜŞÜK"


class RuleType(str, Enum):
    RAKIP_UCUZ = "RAKIP_UCUZ"
    FIYAT_DUSTU = "FIYAT_DUSTU"
    STOK_BITTI = "STOK_BITTI"
    ONERI = "ONERI"


@dataclass
class Alert:
    rule_type: RuleType
    severity: Severity
    product_sku: str
    product_name: str
    competitor_name: str
    current_my_price: float
    current_comp_price: float
    cost: float
    min_margin_pct: float
    message: str
    recommendation: Optional[str] = None
    suggested_price: Optional[float] = None


def evaluate_rules(db: Session) -> List[Alert]:
    """
    Cep-Hane Teknoloji Satın Alma & Fiyatlandırma Kural Motoru:
    Tüm onaylı eşleşmeler için pazaryeri (PttAVM, Hepsiburada, N11/Pazarama) kurallarını çalıştırır:
    - RAKIP_UCUZ: Rakip fiyatı Cep-Hane Kredi Kartı satış fiyatından düşük.
      Havale / Toptan Dip Fiyat Sınırı (maliyet * (1 + min_marj)) kontrol edilerek
      kârlılığı bozmadan inilebilecek optimum fiyat veya "Marjı bozmadan rekabet edemezsin" uyarısı üretilir.
    - FIYAT_DUSTU: Rakip fiyatı bir önceki kayda göre %5 veya daha fazla düştü (Anlık kampanya/indirim).
    - STOK_BITTI: Rakipte ürün stokta yok (Marj koruma / artırma fırsatı).
    - ONERI: Cep-Hane tüm pazaryerlerinden daha ucuzsa 1. sırayı kaybetmeden marj artırma fırsatı.
    """
    alerts: List[Alert] = []

    matches = (
        db.query(Match)
        .filter(Match.durum.in_(["otomatik_onayli", "onayli"]))
        .all()
    )

    product_comp_snapshots: Dict[int, List[Tuple[Competitor, PriceSnapshot]]] = {}

    for match in matches:
        product = db.query(Product).filter(Product.id == match.product_id).first()
        competitor = db.query(Competitor).filter(Competitor.id == match.competitor_id).first()

        if not product or not competitor:
            continue

        snapshots = (
            db.query(PriceSnapshot)
            .filter(
                PriceSnapshot.competitor_id == competitor.id,
                PriceSnapshot.ham_urun_adi == match.ham_urun_adi,
            )
            .order_by(desc(PriceSnapshot.cekilme_zamani), desc(PriceSnapshot.id))
            .limit(2)
            .all()
        )

        if not snapshots:
            continue

        latest_snap = snapshots[0]
        prev_snap = snapshots[1] if len(snapshots) > 1 else None

        product_comp_snapshots.setdefault(product.id, []).append((competitor, latest_snap))

        # Havale / Toptan Dip Fiyat Sınırı: maliyet × (1 + min_marj)
        min_allowed_price = round(product.maliyet * (1.0 + product.min_marj_yuzde / 100.0), 2)

        # ---------------------------------------------------------------------
        # 1. KURAL: STOK_BITTI (Fırsat Uyarısı)
        # ---------------------------------------------------------------------
        if not latest_snap.stokta:
            alerts.append(
                Alert(
                    rule_type=RuleType.STOK_BITTI,
                    severity=Severity.ORTA,
                    product_sku=product.sku,
                    product_name=product.urun_adi,
                    competitor_name=competitor.ad,
                    current_my_price=product.fiyat,
                    current_comp_price=latest_snap.fiyat,
                    cost=product.maliyet,
                    min_margin_pct=product.min_marj_yuzde,
                    message=f"{competitor.ad} kanalında en ucuz rakibin stoğu tükendi. Stok avantajı Cep-Hane Teknoloji'de.",
                    recommendation="Fiyat kırmayın; stok avantajını kullanarak mevcut liste fiyatınızı ve kâr marjınızı koruyun.",
                )
            )

        # ---------------------------------------------------------------------
        # 2. KURAL: FIYAT_DUSTU (Önceki kayda göre %5 veya daha fazla düşüş)
        # ---------------------------------------------------------------------
        if prev_snap and prev_snap.fiyat > 0:
            price_drop = prev_snap.fiyat - latest_snap.fiyat
            drop_pct = (price_drop / prev_snap.fiyat) * 100.0

            if drop_pct >= 5.0:
                alerts.append(
                    Alert(
                        rule_type=RuleType.FIYAT_DUSTU,
                        severity=Severity.YUKSEK,
                        product_sku=product.sku,
                        product_name=product.urun_adi,
                        competitor_name=competitor.ad,
                        current_my_price=product.fiyat,
                        current_comp_price=latest_snap.fiyat,
                        cost=product.maliyet,
                        min_margin_pct=product.min_marj_yuzde,
                        message=(
                            f"Rakip fiyatı önceki kayda göre %{drop_pct:.1f} ({price_drop:.2f} TL) sert düştü "
                            f"({prev_snap.fiyat:.2f} TL ➔ {latest_snap.fiyat:.2f} TL)."
                        ),
                        recommendation=(
                            f"Rakip agresif kampanya başlattı. Havale dip sınırınızı ({min_allowed_price:.2f} TL) "
                            f"kontrol ederek aksiyon alın."
                        ),
                    )
                )

        # ---------------------------------------------------------------------
        # 3. KURAL: RAKIP_UCUZ ve HAVALE DİP MARJ KONTROLÜ
        # ---------------------------------------------------------------------
        if latest_snap.fiyat < product.fiyat:
            diff_tl = product.fiyat - latest_snap.fiyat
            diff_pct = (diff_tl / product.fiyat) * 100.0

            if latest_snap.fiyat <= min_allowed_price:
                suggested_price = round(latest_snap.fiyat * 0.99, 2)
                severity = Severity.YUKSEK
                rec_text = (
                    f"Marjı bozmadan rekabet edemezsin. "
                    f"(Rakip: {latest_snap.fiyat:.2f} TL ≤ Havale Dip Sınırı: {min_allowed_price:.2f} TL | "
                    f"Maliyet: {product.maliyet:.2f} TL, Min Marj: %{product.min_marj_yuzde:.0f})"
                )
            else:
                raw_candidate = round(latest_snap.fiyat * 0.99, 2)
                if raw_candidate >= min_allowed_price:
                    suggested_price = raw_candidate
                else:
                    suggested_price = min_allowed_price

                severity = Severity.YUKSEK if diff_pct >= 2.5 else Severity.ORTA
                calculated_margin = ((suggested_price - product.maliyet) / product.maliyet) * 100.0
                rec_text = (
                    f"Önerilen Fiyat: {suggested_price:.2f} TL "
                    f"(Havale dip sınırınız {min_allowed_price:.2f} TL ve %{calculated_margin:.1f} marj korunarak 1. sıraya geçilir)."
                )

            alerts.append(
                Alert(
                    rule_type=RuleType.RAKIP_UCUZ,
                    severity=severity,
                    product_sku=product.sku,
                    product_name=product.urun_adi,
                    competitor_name=competitor.ad,
                    current_my_price=product.fiyat,
                    current_comp_price=latest_snap.fiyat,
                    cost=product.maliyet,
                    min_margin_pct=product.min_marj_yuzde,
                    message=(
                        f"Rakip fiyatı ({latest_snap.fiyat:.2f} TL), Cep-Hane liste fiyatından ({product.fiyat:.2f} TL) "
                        f"{diff_tl:.2f} TL (%{diff_pct:.1f}) daha ucuz."
                    ),
                    recommendation=rec_text,
                    suggested_price=suggested_price,
                )
            )

    # ---------------------------------------------------------------------
    # 4. KURAL: ONERI (Tüm pazaryerlerinde en ucuz bizsek kâr marjı artırma fırsatı)
    # ---------------------------------------------------------------------
    for prod_id, comp_list in product_comp_snapshots.items():
        product = db.query(Product).filter(Product.id == prod_id).first()
        if not product or not comp_list:
            continue
        cheapest_comp, cheapest_snap = min(comp_list, key=lambda x: x[1].fiyat)
        if cheapest_snap.fiyat > product.fiyat:
            gap_tl = cheapest_snap.fiyat - product.fiyat
            gap_pct = (gap_tl / product.fiyat) * 100.0
            if gap_pct >= 1.0:
                target_price = round(cheapest_snap.fiyat * 0.995, 2)
                if target_price > product.fiyat:
                    extra_profit = round(target_price - product.fiyat, 2)
                    alerts.append(
                        Alert(
                            rule_type=RuleType.ONERI,
                            severity=Severity.DUSUK,
                            product_sku=product.sku,
                            product_name=product.urun_adi,
                            competitor_name=cheapest_comp.ad,
                            current_my_price=product.fiyat,
                            current_comp_price=cheapest_snap.fiyat,
                            cost=product.maliyet,
                            min_margin_pct=product.min_marj_yuzde,
                            message=(
                                f"Pazaryerlerindeki en yakın rakipten ({cheapest_snap.fiyat:.2f} TL) "
                                f"{gap_tl:.2f} TL (%{gap_pct:.1f}) daha ucuzsunuz."
                            ),
                            recommendation=(
                                f"FIRSAT: 1. sırayı kaybetmeden fiyatınızı {target_price:.2f} TL'ye çekerek "
                                f"ürün başına +{extra_profit:.2f} TL ek kâr marjı kazanabilirsiniz."
                            ),
                            suggested_price=target_price,
                        )
                    )

    priority_order = {Severity.YUKSEK: 1, Severity.ORTA: 2, Severity.DUSUK: 3}
    rule_order = {
        RuleType.FIYAT_DUSTU: 1,
        RuleType.RAKIP_UCUZ: 2,
        RuleType.STOK_BITTI: 3,
        RuleType.ONERI: 4,
    }
    alerts.sort(
        key=lambda a: (
            priority_order.get(a.severity, 99),
            rule_order.get(a.rule_type, 99),
        )
    )

    return alerts


def print_alerts_summary(alerts: List[Alert]) -> None:
    """Uyarı listesini terminalde şık ve okunaklı bir şekilde yazdırır."""
    print("\n" + "=" * 95)
    print("🚨 [CEP-HANE TEKNOLOJİ — KURAL MOTORU UYARI VE AKSİYON RAPORU]")
    print(f"Toplam Üretilen Uyarı & Fırsat Sayısı: {len(alerts)}")
    print("=" * 95)

    if not alerts:
        print("✓ Herhangi bir kritik fiyat veya stok uyarısı bulunmamaktadır.")
        return

    for idx, alert in enumerate(alerts, 1):
        icon = "🔴" if alert.severity == Severity.YUKSEK else ("🟡" if alert.severity == Severity.ORTA else "🟢")
        print(f"\n{icon} [{idx}] [{alert.severity.value}] {alert.rule_type.value} | {alert.product_name}")
        print(f"   • Pazaryeri    : {alert.competitor_name}")
        print(f"   • Fiyatlar     : Cep-Hane: {alert.current_my_price:.2f} TL | Rakip: {alert.current_comp_price:.2f} TL")
        print(f"   • Durum        : {alert.message}")
        if alert.recommendation:
            print(f"   • 💡 Tavsiye   : {alert.recommendation}")
        print("-" * 95)


if __name__ == "__main__":
    session = SessionLocal()
    try:
        active_alerts = evaluate_rules(session)
        print_alerts_summary(active_alerts)
    finally:
        session.close()
