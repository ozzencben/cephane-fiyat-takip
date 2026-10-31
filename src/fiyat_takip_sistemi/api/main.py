import io
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from sqlalchemy import desc
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.models import Competitor, Match, PriceSnapshot, Product
from ..core.report import get_latest_report_text
from ..core.seller_profiles import get_seller_profile
from ..scripts.seed_history import seed_price_history

app = FastAPI(
    title="Cep-Hane Teknoloji | Fiyat Takip ve Rekabet Paneli API",
    description="Pazaryeri satıcı karşılaştırma, günlük yapay zeka raporu, Excel çıktı ve fiyat geçmişi API uç noktaları.",
    version="2.0.0",
)

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def format_tr_price(val: Optional[float], signed: bool = False) -> str:
    if val is None:
        return "-"
    s = f"{val:+,.2f}" if signed else f"{val:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


templates.env.filters["tr_fiyat"] = lambda v: format_tr_price(v, signed=False)
templates.env.filters["tr_fark"] = lambda v: format_tr_price(v, signed=True)


def _get_competitor_role_map(db: Session) -> Dict[int, str]:
    """Rakip ID'lerini rakip_a (PttAVM), rakip_b (Hepsiburada), rakip_c (N11/Pazarama) ile eşleştirir."""
    role_map: Dict[int, str] = {}
    for comp in db.query(Competitor).all():
        ad_lower = comp.ad.lower()
        if "pttavm" in ad_lower or "rakip a" in ad_lower or "bookstoscrape" in ad_lower:
            role_map[comp.id] = "rakip_a"
        elif "hepsiburada" in ad_lower or "rakip b" in ad_lower or "webscraper" in ad_lower:
            role_map[comp.id] = "rakip_b"
        elif "n11" in ad_lower or "pazarama" in ad_lower or "rakip c" in ad_lower or "sahte magaza" in ad_lower:
            role_map[comp.id] = "rakip_c"
    return role_map


def _build_product_comparison_item(
    db: Session,
    product: Product,
    competitors_by_id: Dict[int, Competitor],
    role_map: Dict[int, str],
) -> Dict[str, Any]:
    """Tek bir ürün için onaylı pazaryeri fiyatlarını, satıcı mağaza profillerini, farkı ve fiyat önerisini hesaplar."""
    matches = (
        db.query(Match)
        .filter(
            Match.product_id == product.id,
            Match.durum.in_(["otomatik_onayli", "onayli"]),
        )
        .all()
    )

    rakip_prices_by_role: Dict[str, Optional[float]] = {
        "rakip_a": None,
        "rakip_b": None,
        "rakip_c": None,
    }
    rakip_detay_by_role: Dict[str, Optional[Dict[str, Any]]] = {
        "rakip_a": None,
        "rakip_b": None,
        "rakip_c": None,
    }
    competitor_details: List[Dict[str, Any]] = []

    min_allowed_price = round(
        product.maliyet * (1.0 + product.min_marj_yuzde / 100.0), 2
    )

    for match in matches:
        latest_snap = (
            db.query(PriceSnapshot)
            .filter(
                PriceSnapshot.competitor_id == match.competitor_id,
                PriceSnapshot.ham_urun_adi == match.ham_urun_adi,
            )
            .order_by(desc(PriceSnapshot.cekilme_zamani), desc(PriceSnapshot.id))
            .first()
        )
        if not latest_snap:
            continue

        comp = competitors_by_id.get(match.competitor_id)
        comp_name = comp.ad if comp else f"Rakip #{match.competitor_id}"
        role_key = role_map.get(match.competitor_id)
        seller_prof = get_seller_profile(product.sku, comp_name, latest_snap.stokta)

        dip_fark = round(latest_snap.fiyat - min_allowed_price, 2)
        detail_obj = {
            "competitor_id": match.competitor_id,
            "rakip_adi": comp_name,
            "kanal": seller_prof["kanal"],
            "satici": seller_prof["satici"],
            "puan": seller_prof["puan"],
            "stok_notu": seller_prof["stok_notu"],
            "kargo": seller_prof["kargo"],
            "etiket": seller_prof["etiket"],
            "ham_urun_adi": match.ham_urun_adi,
            "fiyat": latest_snap.fiyat,
            "stokta": latest_snap.stokta,
            "dip_fark": dip_fark,
            "dip_alti": latest_snap.fiyat <= min_allowed_price,
            "url": latest_snap.url,
            "cekilme_zamani": latest_snap.cekilme_zamani.strftime("%Y-%m-%d %H:%M:%S")
            if latest_snap.cekilme_zamani
            else None,
        }

        if role_key:
            rakip_prices_by_role[role_key] = latest_snap.fiyat
            rakip_detay_by_role[role_key] = detail_obj

        competitor_details.append(detail_obj)

    valid_details = [c for c in competitor_details if c["fiyat"] is not None]
    cheapest_detail: Optional[Dict[str, Any]] = (
        min(valid_details, key=lambda x: x["fiyat"]) if valid_details else None
    )
    min_comp_price: Optional[float] = cheapest_detail["fiyat"] if cheapest_detail else None

    fark: Optional[float] = None
    fark_yuzde: Optional[float] = None
    durum = "VERİ YOK"
    onerilen_fiyat: Optional[float] = None
    yeni_marj_yuzde: Optional[float] = None
    oneri_notu: Optional[str] = None
    dip_alti = False

    if min_comp_price is not None:
        fark = round(min_comp_price - product.fiyat, 2)
        fark_yuzde = round((fark / product.fiyat) * 100.0, 1) if product.fiyat > 0 else 0.0

        if min_comp_price < product.fiyat:
            durum = "RAKİP UCUZ"
            if min_comp_price <= min_allowed_price:
                dip_alti = True
                candidate_price = round(min_comp_price * 0.99, 2)
                onerilen_fiyat = candidate_price
                oneri_notu = (
                    f"⛔ Marjı bozmadan rekabet edilemez "
                    f"(Rakip: {format_tr_price(min_comp_price)} TL ≤ Havale Dip: {format_tr_price(min_allowed_price)} TL)"
                )
            else:
                raw_cand = round(min_comp_price * 0.99, 2)
                candidate_price = raw_cand if raw_cand >= min_allowed_price else min_allowed_price
                onerilen_fiyat = candidate_price
                safe_margin = ((candidate_price - product.maliyet) / product.maliyet) * 100.0
                yeni_marj_yuzde = round(safe_margin, 1)
                oneri_notu = (
                    f"🎯 Önerilen: {format_tr_price(candidate_price)} TL "
                    f"(Havale dip korunur, %{safe_margin:.1f} marj ile 1. sıra alınır)"
                )
        elif min_comp_price > product.fiyat:
            durum = "BİZ UCUZUZ"
            target_fiyat = round(min_comp_price * 0.995, 2)
            if target_fiyat > product.fiyat:
                ek_kar = round(target_fiyat - product.fiyat, 2)
                onerilen_fiyat = target_fiyat
                safe_margin = ((target_fiyat - product.maliyet) / product.maliyet) * 100.0
                yeni_marj_yuzde = round(safe_margin, 1)
                oneri_notu = (
                    f"💡 FIRSAT: 1. sırayı kaybetmeden {format_tr_price(target_fiyat)} TL'ye çekilebilir "
                    f"(+{format_tr_price(ek_kar)} TL ek kâr)"
                )
            else:
                oneri_notu = "Fiyat avantajı bizde; mevcut liste fiyatı korunabilir."
        else:
            durum = "EŞİT"
            oneri_notu = "Rakip ile fiyat eşit."

    return {
        "id": product.id,
        "sku": product.sku,
        "urun_adi": product.urun_adi,
        "benim_fiyatim": product.fiyat,
        "maliyet": product.maliyet,
        "min_marj_yuzde": product.min_marj_yuzde,
        "min_kabul_edilebilir_fiyat": min_allowed_price,
        "rakip_a": rakip_prices_by_role["rakip_a"],
        "rakip_b": rakip_prices_by_role["rakip_b"],
        "rakip_c": rakip_prices_by_role["rakip_c"],
        "rakip_a_detay": rakip_detay_by_role["rakip_a"],
        "rakip_b_detay": rakip_detay_by_role["rakip_b"],
        "rakip_c_detay": rakip_detay_by_role["rakip_c"],
        "en_dusuk_rakip_fiyat": min_comp_price,
        "en_ucuz_rakip_detay": cheapest_detail,
        "fark": fark,
        "fark_yuzde": fark_yuzde,
        "durum": durum,
        "dip_alti": dip_alti,
        "onerilen_fiyat": onerilen_fiyat,
        "yeni_marj_yuzde": yeni_marj_yuzde,
        "oneri_notu": oneri_notu,
        "rakip_fiyatlari": competitor_details,
    }


@app.get("/", response_class=HTMLResponse, tags=["Web Paneli"])
def get_dashboard_home(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    ozet_data = get_ozet(db=db)
    urunler_data = get_urunler(db=db)
    dip_alti_sayisi = sum(1 for u in urunler_data if u.get("dip_alti"))
    firsat_sayisi = sum(1 for u in urunler_data if u.get("durum") == "BİZ UCUZUZ")
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "ozet": ozet_data,
            "urunler": urunler_data,
            "dip_alti_sayisi": dip_alti_sayisi,
            "firsat_sayisi": firsat_sayisi,
        },
    )


@app.get("/indir/onerilen-fiyatlar.xlsx", tags=["Excel İndir"])
def download_recommended_prices_excel(db: Session = Depends(get_db)):
    """
    Cep-Hane Teknoloji Satın Alma Müdürlüğü ve PraPazar entegrasyonu için
    tüm pazaryeri satıcı analizlerini ve önerilen yeni fiyatları Excel (.xlsx) olarak indirir.
    """
    urunler_data = get_urunler(db=db)

    wb = Workbook()
    ws = wb.active
    ws.title = "Cep-Hane Fiyat Önerileri"

    headers = [
        "SKU",
        "Ürün Adı",
        "Cep-Hane Liste Fiyatı (TL)",
        "Havale / Dip Sınırı (TL)",
        "PttAVM En Ucuz (Satıcı & Fiyat)",
        "Hepsiburada En Ucuz (Satıcı & Fiyat)",
        "N11 / Pazarama En Ucuz (Satıcı & Fiyat)",
        "En Ucuz Rakip Kanal & Mağaza",
        "En Ucuz Rakip Fiyatı (TL)",
        "Rekabet Durumu",
        "Sistemin Önerdiği Fiyat (TL)",
        "Satın Alma Aksiyon Notu",
    ]
    ws.append(headers)

    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=11)
    thin_border = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1"),
    )

    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    def _fmt_cell(det: Optional[Dict[str, Any]]) -> str:
        if not det or det.get("fiyat") is None:
            return "Onay Bekliyor"
        return f"{format_tr_price(det['fiyat'])} TL ({det['satici']} ★{det['puan']})"

    for u in urunler_data:
        cheapest = u.get("en_ucuz_rakip_detay")
        cheapest_label = cheapest["etiket"] if cheapest else "-"
        onerilen = u.get("onerilen_fiyat") if not u.get("dip_alti") else u.get("benim_fiyatim")

        row = [
            u["sku"],
            u["urun_adi"],
            u["benim_fiyatim"],
            u["min_kabul_edilebilir_fiyat"],
            _fmt_cell(u.get("rakip_a_detay")),
            _fmt_cell(u.get("rakip_b_detay")),
            _fmt_cell(u.get("rakip_c_detay")),
            cheapest_label,
            u.get("en_dusuk_rakip_fiyat") or 0.0,
            "EN UCUZ BİZİZ" if u["durum"] == "BİZ UCUZUZ" else u["durum"],
            onerilen or u["benim_fiyatim"],
            u.get("oneri_notu") or "",
        ]
        ws.append(row)

    for row_cells in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=len(headers)):
        for c in row_cells:
            c.border = thin_border
            c.alignment = Alignment(vertical="center")

    col_widths = [12, 52, 22, 22, 32, 32, 32, 30, 22, 18, 24, 58]
    for i, w in enumerate(col_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = w

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)

    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="CepHane_Onerilen_Fiyat_Listesi.xlsx"'
        },
    )


@app.get("/urun/{id}", response_class=HTMLResponse, tags=["Web Paneli"])
def get_product_detail_page(
    id: int, request: Request, db: Session = Depends(get_db)
) -> HTMLResponse:
    gecmis_data = get_urun_gecmis(id=id, db=db)
    product = db.query(Product).filter(Product.id == id).first()
    competitors_by_id = {c.id: c for c in db.query(Competitor).all()}
    role_map = _get_competitor_role_map(db)
    karsilastirma = _build_product_comparison_item(
        db, product, competitors_by_id, role_map
    )

    return templates.TemplateResponse(
        request=request,
        name="product_detail.html",
        context={
            "detay": gecmis_data,
            "karsilastirma": karsilastirma,
        },
    )


def _serialize_match_row(
    db: Session,
    match: Match,
    products_by_id: Dict[int, Product],
    competitors_by_id: Dict[int, Competitor],
) -> Dict[str, Any]:
    prod = products_by_id.get(match.product_id)
    comp = competitors_by_id.get(match.competitor_id)

    latest_snap = (
        db.query(PriceSnapshot)
        .filter(
            PriceSnapshot.competitor_id == match.competitor_id,
            PriceSnapshot.ham_urun_adi == match.ham_urun_adi,
        )
        .order_by(desc(PriceSnapshot.cekilme_zamani), desc(PriceSnapshot.id))
        .first()
    )

    comp_name = comp.ad if comp else f"Rakip #{match.competitor_id}"
    seller_prof = get_seller_profile(prod.sku if prod else "CPH-001", comp_name, latest_snap.stokta if latest_snap else True)

    if match.skor >= 80.0:
        oneri_metni = (
            f"Öneri: Aynı ürün (Benzerlik %{match.skor:.0f}, model kodu/kısaltma farkı görünüyor)"
        )
    else:
        oneri_metni = (
            f"Öneri: Kontrol edin (Benzerlik %{match.skor:.0f}, anahtar kelimeler örtüşüyor)"
        )

    return {
        "match_id": match.id,
        "product_id": match.product_id,
        "sku": prod.sku if prod else "-",
        "urun_adi": prod.urun_adi if prod else "Bilinmeyen Ürün",
        "benim_fiyatim": prod.fiyat if prod else 0.0,
        "competitor_id": match.competitor_id,
        "rakip_adi": seller_prof["etiket"],
        "ham_urun_adi": match.ham_urun_adi,
        "rakip_fiyat": latest_snap.fiyat if latest_snap else None,
        "skor": match.skor,
        "durum": match.durum,
        "oneri_metni": oneri_metni,
    }


@app.get("/eslesmeler", response_class=HTMLResponse, tags=["Web Paneli"])
def get_matches_review_page(
    request: Request, db: Session = Depends(get_db)
) -> HTMLResponse:
    products_by_id = {p.id: p for p in db.query(Product).all()}
    competitors_by_id = {c.id: c for c in db.query(Competitor).all()}

    pending_rows = (
        db.query(Match)
        .filter(Match.durum == "onay_bekliyor")
        .order_by(desc(Match.skor), Match.id.asc())
        .all()
    )
    decided_rows = (
        db.query(Match)
        .filter(Match.durum.in_(["onayli", "reddedildi"]))
        .order_by(desc(Match.id))
        .all()
    )

    bekleyenler = [
        _serialize_match_row(db, m, products_by_id, competitors_by_id)
        for m in pending_rows
    ]
    tamamlananlar = [
        _serialize_match_row(db, m, products_by_id, competitors_by_id)
        for m in decided_rows
    ]

    return templates.TemplateResponse(
        request=request,
        name="matches.html",
        context={
            "bekleyenler": bekleyenler,
            "tamamlananlar": tamamlananlar,
        },
    )


@app.post("/eslesmeler/{match_id}/karar", tags=["Web Paneli"])
async def post_match_decision(
    match_id: int, request: Request, db: Session = Depends(get_db)
):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=404, detail=f"ID={match_id} olan eşleşme bulunamadı."
        )

    raw_body = (await request.body()).decode("utf-8", errors="replace").strip()
    karar_val = ""
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type and raw_body:
        try:
            body_json = json.loads(raw_body)
            karar_val = str(body_json.get("karar", "")).strip()
        except Exception:
            pass

    if not karar_val and raw_body:
        parsed_form = parse_qs(raw_body)
        if "karar" in parsed_form and parsed_form["karar"]:
            karar_val = parsed_form["karar"][0].strip()

    if not karar_val:
        karar_val = str(request.query_params.get("karar", "")).strip()

    normalized = karar_val.lower()
    if normalized in ("onayli", "onayla", "ayni", "ayni_urun", "approve"):
        match.durum = "onayli"
    elif normalized in ("reddedildi", "reddet", "farkli", "farkli_urun", "reject"):
        match.durum = "reddedildi"
    else:
        raise HTTPException(
            status_code=400,
            detail="Geçersiz karar değeri. 'onayli' veya 'reddedildi' gönderilmelidir.",
        )

    db.commit()
    db.refresh(match)

    if match.durum == "onayli":
        product = db.query(Product).filter(Product.id == match.product_id).first()
        latest_snap = (
            db.query(PriceSnapshot)
            .filter(
                PriceSnapshot.competitor_id == match.competitor_id,
                PriceSnapshot.ham_urun_adi == match.ham_urun_adi,
            )
            .order_by(desc(PriceSnapshot.cekilme_zamani), desc(PriceSnapshot.id))
            .first()
        )
        existing_count = (
            db.query(PriceSnapshot)
            .filter(
                PriceSnapshot.competitor_id == match.competitor_id,
                PriceSnapshot.ham_urun_adi == match.ham_urun_adi,
            )
            .count()
        )
        if product and existing_count < 10:
            seed_price_history(
                db=db,
                competitor_id=match.competitor_id,
                ham_urun_adi=match.ham_urun_adi,
                base_price=latest_snap.fiyat if latest_snap else product.fiyat,
                url=latest_snap.url if latest_snap else "",
                days=14,
            )

    accept_header = request.headers.get("accept", "")
    if "application/json" in accept_header and "text/html" not in accept_header:
        return {
            "basarili": True,
            "match_id": match.id,
            "yeni_durum": match.durum,
        }

    return RedirectResponse(url="/eslesmeler", status_code=303)


@app.get("/api/ozet", tags=["API"])
def get_ozet(db: Session = Depends(get_db)) -> Dict[str, Any]:
    products = db.query(Product).all()
    toplam_urun = len(products)

    competitors_by_id = {c.id: c for c in db.query(Competitor).all()}
    role_map = _get_competitor_role_map(db)

    rakibin_ucuz_oldugu_sayisi = 0
    for prod in products:
        comp_item = _build_product_comparison_item(
            db, prod, competitors_by_id, role_map
        )
        if comp_item["durum"] == "RAKİP UCUZ":
            rakibin_ucuz_oldugu_sayisi += 1

    latest_snap = (
        db.query(PriceSnapshot)
        .order_by(desc(PriceSnapshot.cekilme_zamani), desc(PriceSnapshot.id))
        .first()
    )
    son_guncelleme = (
        latest_snap.cekilme_zamani.strftime("%Y-%m-%d %H:%M:%S")
        if latest_snap and latest_snap.cekilme_zamani
        else "Henüz veri yok"
    )

    onay_bekleyen_sayisi = (
        db.query(Match).filter(Match.durum == "onay_bekliyor").count()
    )

    son_rapor_metni = get_latest_report_text(db)

    return {
        "toplam_urun": toplam_urun,
        "rakibin_ucuz_oldugu_urun_sayisi": rakibin_ucuz_oldugu_sayisi,
        "bizim_avantajli_oldugumuz_urun_sayisi": max(
            0, toplam_urun - rakibin_ucuz_oldugu_sayisi
        ),
        "onay_bekleyen_eslesme_sayisi": onay_bekleyen_sayisi,
        "son_guncelleme_zamani": son_guncelleme,
        "son_rapor": son_rapor_metni,
    }


@app.get("/api/urunler", tags=["API"])
def get_urunler(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    products = db.query(Product).order_by(Product.id.asc()).all()
    if not products:
        return []

    competitors_by_id = {c.id: c for c in db.query(Competitor).all()}
    role_map = _get_competitor_role_map(db)

    result: List[Dict[str, Any]] = []
    for prod in products:
        item = _build_product_comparison_item(db, prod, competitors_by_id, role_map)
        result.append(item)

    return result


@app.get("/api/urunler/{id}/gecmis", tags=["API"])
def get_urun_gecmis(id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"ID={id} olan ürün bulunamadı.")

    competitors_by_id = {c.id: c for c in db.query(Competitor).all()}
    matches = (
        db.query(Match)
        .filter(
            Match.product_id == product.id,
            Match.durum.in_(["otomatik_onayli", "onayli"]),
        )
        .all()
    )

    rakipler_gecmis: List[Dict[str, Any]] = []
    tum_gecmis_kayitlari: List[Dict[str, Any]] = []

    for match in matches:
        comp = competitors_by_id.get(match.competitor_id)
        comp_name = comp.ad if comp else f"Rakip #{match.competitor_id}"
        seller_prof = get_seller_profile(product.sku, comp_name, True)

        snapshots = (
            db.query(PriceSnapshot)
            .filter(
                PriceSnapshot.competitor_id == match.competitor_id,
                PriceSnapshot.ham_urun_adi == match.ham_urun_adi,
            )
            .order_by(PriceSnapshot.cekilme_zamani.asc(), PriceSnapshot.id.asc())
            .all()
        )

        kayitlar = []
        for snap in snapshots:
            tarih_str = (
                snap.cekilme_zamani.strftime("%Y-%m-%d %H:%M:%S")
                if snap.cekilme_zamani
                else None
            )
            kayit_item = {
                "snapshot_id": snap.id,
                "fiyat": snap.fiyat,
                "stokta": snap.stokta,
                "cekilme_zamani": tarih_str,
                "url": snap.url,
            }
            kayitlar.append(kayit_item)
            tum_gecmis_kayitlari.append({
                "snapshot_id": snap.id,
                "competitor_id": match.competitor_id,
                "rakip_adi": seller_prof["etiket"],
                "ham_urun_adi": match.ham_urun_adi,
                "fiyat": snap.fiyat,
                "stokta": snap.stokta,
                "cekilme_zamani": tarih_str,
            })

        rakipler_gecmis.append({
            "competitor_id": match.competitor_id,
            "rakip_adi": seller_prof["etiket"],
            "ham_urun_adi": match.ham_urun_adi,
            "eslesme_skoru": match.skor,
            "eslesme_durumu": match.durum,
            "kayitlar": kayitlar,
        })

    tum_gecmis_kayitlari.sort(key=lambda x: (x.get("cekilme_zamani") or "", x.get("snapshot_id") or 0))

    min_allowed_price = round(
        product.maliyet * (1.0 + product.min_marj_yuzde / 100.0), 2
    )

    return {
        "urun": {
            "id": product.id,
            "sku": product.sku,
            "urun_adi": product.urun_adi,
            "benim_fiyatim": product.fiyat,
            "maliyet": product.maliyet,
            "min_marj_yuzde": product.min_marj_yuzde,
            "min_kabul_edilebilir_fiyat": min_allowed_price,
        },
        "rakipler": rakipler_gecmis,
        "gecmis": tum_gecmis_kayitlari,
    }


@app.post("/demo/fiyat-dusur", tags=["Canlı Demo Aksiyonları"])
def post_demo_price_drop(db: Session = Depends(get_db)):
    from datetime import datetime
    from ..core.report import prepare_report_data, run_daily_report
    from ..core.notify import format_daily_notification_message, send_telegram_message

    comp_c = (
        db.query(Competitor)
        .filter(Competitor.ad.ilike("%N11%"))
        .first()
        or db.query(Competitor).order_by(Competitor.id.desc()).first()
    )
    target_name = "Apple iPhone 15 128 GB (Apple Türkiye Garantili) Siyah"
    if comp_c:
        latest = (
            db.query(PriceSnapshot)
            .filter(
                PriceSnapshot.competitor_id == comp_c.id,
                PriceSnapshot.ham_urun_adi == target_name,
            )
            .order_by(desc(PriceSnapshot.cekilme_zamani), desc(PriceSnapshot.id))
            .first()
        )
        old_price = latest.fiyat if latest else 59600.0
        new_price = round(old_price * 0.85, 2)
        snap = PriceSnapshot(
            competitor_id=comp_c.id,
            ham_urun_adi=target_name,
            fiyat=new_price,
            stokta=True,
            url="http://localhost:8001/urun/1",
            cekilme_zamani=datetime.now(),
        )
        db.add(snap)
        db.commit()

    rep_text = run_daily_report(db)
    rep_data = prepare_report_data(db)
    tg_msg = format_daily_notification_message(rep_text, rep_data.get("en_kritik_uyarilar", []))
    send_telegram_message(tg_msg)

    return RedirectResponse(url="/?bildirim=indirim_simule_edildi", status_code=303)


@app.post("/demo/telegram-gonder", tags=["Canlı Demo Aksiyonları"])
def post_demo_send_telegram(db: Session = Depends(get_db)):
    from ..core.report import get_latest_report_text, prepare_report_data
    from ..core.notify import format_daily_notification_message, send_telegram_message

    rep_text = get_latest_report_text(db)
    rep_data = prepare_report_data(db)
    tg_msg = format_daily_notification_message(rep_text, rep_data.get("en_kritik_uyarilar", []))
    send_telegram_message(tg_msg)

    return RedirectResponse(url="/?bildirim=telegram_gonderildi", status_code=303)


@app.post("/demo/sifirla", tags=["Canlı Demo Aksiyonları"])
def post_demo_reset(db: Session = Depends(get_db)):
    db.close()
    from ..scripts.demo_reset import reset_demo_environment
    reset_demo_environment()
    return RedirectResponse(url="/?bildirim=demo_sifirlandi", status_code=303)


@app.get("/health", tags=["Sistem"])
def health_check():
    """UptimeRobot / Cron-job.org 7/24 uyanık tutma (keep-alive) uç noktası."""
    return {"status": "ok", "service": "cephane-fiyat-takip"}


@app.on_event("startup")
def on_startup_ensure_demo_data():
    """
    Bulut sunucusu (Render) ilk kez ayağa kalktığında veya yeniden başladığında
    veritabanı boşsa otomatik olarak 12 Cep-Hane ürününü, pazaryeri satıcılarını
    ve 14 günlük geçmişi hazırlar; ayrıca RENDER_EXTERNAL_URL varsa 10 dakikada bir
    otomatik keep-alive ping döngüsünü başlatır.
    """
    import os
    import threading
    import time
    import httpx
    from ..core.db import Base, SessionLocal, engine
    from ..core.models import Product

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        count = db.query(Product).count()
    except Exception:
        count = 0
    finally:
        db.close()

    if count == 0:
        print("🚀 [STARTUP] Veritabanı boş, Cep-Hane Teknoloji demo verileri otomatik yükleniyor...")
        from ..scripts.demo_reset import reset_demo_environment
        reset_demo_environment()

    ext_url = os.getenv("RENDER_EXTERNAL_URL", "").strip()
    if ext_url:
        def _keep_alive_worker(url: str):
            ping_target = url.rstrip("/") + "/health"
            while True:
                time.sleep(600)  # 10 dakika
                try:
                    httpx.get(ping_target, timeout=15.0)
                except Exception:
                    pass

        t = threading.Thread(target=_keep_alive_worker, args=(ext_url,), daemon=True)
        t.start()
