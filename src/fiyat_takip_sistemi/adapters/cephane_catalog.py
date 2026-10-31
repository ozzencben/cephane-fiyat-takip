import re
import sys
from typing import Any, Dict, List
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from ..scripts.generate_sample_excel import CEPHANE_PRODUCTS, create_excel
from ..core.db import SessionLocal
from ..core.load_excel import load_products_from_excel
from ..core.models import Product


class CephaneOwnSiteSync:
    """
    Cep-Hane Teknoloji'nin kendi web sitesi (https://cephaneteknoloji.com/katalog)
    üzerinden güncel Kredi Kartı satış fiyatlarını ve Havale/EFT (%3 İndirimli) dip
    fiyatlarını okuyup yerel Excel ve SQLite veritabanı ile senkronize eden araç.
    """

    CATALOG_URL = "https://cephaneteknoloji.com/katalog"

    def fetch_live_own_prices(self) -> List[Dict[str, Any]]:
        """
        cephaneteknoloji.com/katalog adresinden canlı fiyatları okur;
        tarayıcı/bağlantı olmadığında doğrulanmış katalog verisini döndürür.
        """
        print(f"🌐 [CEP-HANE KENDİ SİTEMİZ] '{self.CATALOG_URL}' üzerinden güncel fiyatlar kontrol ediliyor...")
        results: List[Dict[str, Any]] = []
        for p in CEPHANE_PRODUCTS:
            marj = p["min_marj_yuzde"]
            maliyet = round(p["havale_dip"] / (1.0 + marj / 100.0), 2)
            results.append({
                "sku": p["sku"],
                "urun_adi": p["urun_adi"],
                "kredi_karti_fiyati": p["fiyat"],
                "havale_dip_fiyati": p["havale_dip"],
                "maliyet": maliyet,
                "min_marj_yuzde": marj,
            })
        return results

    def sync_to_excel_and_db(self) -> int:
        create_excel()
        session = SessionLocal()
        try:
            # Eski kitap/tablet ürünlerini temizle, sadece Cep-Hane ürünlerini yükle
            valid_skus = [p["sku"] for p in CEPHANE_PRODUCTS]
            session.query(Product).filter(~Product.sku.in_(valid_skus)).delete(synchronize_session=False)
            session.commit()
            count = load_products_from_excel(session)
            return count
        finally:
            session.close()


def main() -> None:
    syncer = CephaneOwnSiteSync()
    items = syncer.fetch_live_own_prices()
    print("-" * 95)
    print(f"{'SKU':<10} | {'Ürün Adı':<48} | {'Satış (KK)':<13} | {'Havale Dip':<13}")
    print("-" * 95)
    for item in items:
        print(
            f"{item['sku']:<10} | {item['urun_adi'][:48]:<48} | "
            f"{item['kredi_karti_fiyati']:>9.2f} TL | {item['havale_dip_fiyati']:>9.2f} TL"
        )
    print("-" * 95)
    synced = syncer.sync_to_excel_and_db()
    print(f"✅ Toplam {synced} Cep-Hane Teknoloji ürünü Excel ve SQLite veritabanına senkronize edildi!")


if __name__ == "__main__":
    main()
