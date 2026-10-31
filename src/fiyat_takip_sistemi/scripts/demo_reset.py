import json
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from ..adapters.books_toscrape import BooksToScrapeAdapter, PTTAVM_LISTINGS
from ..adapters.fake_store import FakeStoreAdapter
from ..adapters.webscraper_io import WebScraperIOAdapter, HEPSIBURADA_LISTINGS
from ..core.db import Base, SessionLocal, engine
from ..core.load_excel import load_products_from_excel
from ..core.matching import run_product_matching
from ..core.models import Competitor, PriceSnapshot
from ..core.report import prepare_report_data, save_last_report
from .generate_sample_excel import create_excel
from .seed_history import seed_price_history

PROJECT_ROOT = Path(__file__).resolve().parents[3]
PRICES_JSON_PATH = PROJECT_ROOT / "data" / "prices.json"

INITIAL_N11_PAZARAMA_PRODUCTS = [
    {"id": 1, "name": "Apple iPhone 15 128 GB (Apple Türkiye Garantili) Siyah", "price": 58750.00, "in_stock": True, "url": "http://localhost:8001/products/1"},
    {"id": 2, "name": "Apple iPhone 16e 128 GB (Apple Türkiye Garantili) Beyaz", "price": 52400.00, "in_stock": True, "url": "http://localhost:8001/products/2"},
    {"id": 3, "name": "Apple iPhone 16 Plus 128 GB (Apple Türkiye Garantili) Yeşil", "price": 82490.00, "in_stock": True, "url": "http://localhost:8001/products/3"},
    {"id": 4, "name": "Samsung Galaxy A36 128 GB 8 GB RAM 5G (Samsung Türkiye Garantili) Gri", "price": 25250.00, "in_stock": True, "url": "http://localhost:8001/products/4"},
    {"id": 5, "name": "Samsung Galaxy A26 256 GB 8 GB RAM 5G (Samsung Türkiye Garantili) Beyaz", "price": 23390.00, "in_stock": True, "url": "http://localhost:8001/products/5"},
    {"id": 6, "name": "Samsung Galaxy A17 128 GB 6 GB RAM 5G (Samsung Türkiye Garantili) Gri", "price": 15250.00, "in_stock": True, "url": "http://localhost:8001/products/6"},
    {"id": 7, "name": "POCO X8 Pro 256 GB 8 GB RAM (Distribütör Garantili) Beyaz", "price": 33950.00, "in_stock": True, "url": "http://localhost:8001/products/7"},
    {"id": 8, "name": "Apple iPad Mini 7 512 GB Wi-Fi + Cellular 8.3 inç Tablet Mavi", "price": 59100.00, "in_stock": False, "url": "http://localhost:8001/products/8"},
    {"id": 9, "name": "Xiaomi Redmi Pad 2 64 GB 4 GB RAM 9.7 inç (Xiaomi Türkiye Garantili) Gri", "price": 7290.00, "in_stock": True, "url": "http://localhost:8001/products/9"},
    {"id": 10, "name": "Samsung Watch 8 44 MM Akıllı Saat (Samsung Türkiye Garantili) Koyu Gri", "price": 12290.00, "in_stock": True, "url": "http://localhost:8001/products/10"},
    {"id": 11, "name": "Apple AirPods Pro 3 Bluetooth Kulaklık Beyaz", "price": 13650.00, "in_stock": True, "url": "http://localhost:8001/products/11"},
    {"id": 12, "name": "Apple 20W USB-C Güç Adaptörü (Apple Türkiye Garantili) Beyaz", "price": 939.00, "in_stock": True, "url": "http://localhost:8001/products/12"},
]


def reset_demo_state() -> None:
    print("=" * 80)
    print("🔄 [CEP-HANE DEMO SIFIRLAMA] Sistem temiz başlangıç durumuna getiriliyor...")
    print("=" * 80)

    PRICES_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PRICES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(INITIAL_N11_PAZARAMA_PRODUCTS, f, ensure_ascii=False, indent=2)
    print(f"✓ N11 / Pazarama simülasyon fiyatları ({len(INITIAL_N11_PAZARAMA_PRODUCTS)} ürün) başlangıç değerlerine döndürüldü.")

    create_excel()

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✓ Veritabanı tabloları temizlendi ve yeniden oluşturuldu.")

    session = SessionLocal()
    try:
        prod_count = load_products_from_excel(session)
        print(f"✓ Excel'den {prod_count} Cep-Hane Teknoloji ürünü veritabanına yüklendi.")

        comp_a = Competitor(ad=BooksToScrapeAdapter.COMPETITOR_NAME, base_url=BooksToScrapeAdapter.BASE_URL)
        comp_c = Competitor(ad=FakeStoreAdapter.COMPETITOR_NAME, base_url=FakeStoreAdapter.BASE_URL)
        comp_b = Competitor(ad=WebScraperIOAdapter.COMPETITOR_NAME, base_url=WebScraperIOAdapter.BASE_URL)
        session.add_all([comp_a, comp_c, comp_b])
        session.commit()
        session.refresh(comp_a)
        session.refresh(comp_c)
        session.refresh(comp_b)

        now = datetime.utcnow()
        for item in PTTAVM_LISTINGS:
            session.add(
                PriceSnapshot(
                    competitor_id=comp_a.id,
                    ham_urun_adi=item["name"],
                    url=item["url"],
                    fiyat=item["price"],
                    stokta=bool(item.get("in_stock", True)),
                    cekilme_zamani=now,
                )
            )
        for item in INITIAL_N11_PAZARAMA_PRODUCTS:
            session.add(
                PriceSnapshot(
                    competitor_id=comp_c.id,
                    ham_urun_adi=item["name"],
                    url=item["url"],
                    fiyat=item["price"],
                    stokta=bool(item.get("in_stock", True)),
                    cekilme_zamani=now,
                )
            )
        for item in HEPSIBURADA_LISTINGS:
            session.add(
                PriceSnapshot(
                    competitor_id=comp_b.id,
                    ham_urun_adi=item["name"],
                    url=item["url"],
                    fiyat=item["price"],
                    stokta=bool(item.get("in_stock", True)),
                    cekilme_zamani=now,
                )
            )
        session.commit()
        print("✓ 3 pazaryeri kanalının (PttAVM, Hepsiburada, N11/Pazarama) başlangıç fiyatları yüklendi.")

        run_product_matching(session)
        seed_price_history(session, days=14)

        report_data = prepare_report_data(session)
        baseline_llm_report = (
            f"{report_data.get('rapor_tarihi', '')[:10]} tarihli Cep-Hane Teknoloji fiyat takip verilerine göre, "
            f"izlenen {report_data.get('toplam_urun_sayisi', 12)} ana ürünümüzün "
            f"{report_data.get('rakibin_ucuz_oldugu_urun_sayisi', 9)} tanesinde pazaryeri rakiplerimiz (PttAVM, Hepsiburada, N11/Pazarama) "
            f"liste fiyatımızın altında satış yaparken, {report_data.get('avantajli_urun_sayisi', 3)} üründe en ucuz satıcı konumundayız. "
            "Özellikle 'Apple iPhone 15 128 GB Siyah', 'Apple iPhone 16 Plus 128 GB' ve 'POCO X8 Pro 256 GB' modellerinde "
            "Havale/EFT dip fiyat sınırımızı koruyarak pazaryerinde 1. sıraya (en ucuz satıcı konumuna) geçebileceğimiz güvenli marj alanı bulunmaktadır. "
            "Buna karşın 'Samsung Galaxy A17' ve 'Samsung Watch 8 44mm' ürünlerinde rakipler toptan/havale dip sınırımızın yakınına indiğinden "
            "kârlılığı bozmamak adına ek fiyat kırılmaması önerilir.\n\n"
            "Satın Alma ve Fiyatlandırma Aksiyon Önerileri:\n"
            "1. 'Apple iPhone 15 128 GB Siyah' (Önerilen: 58.650,00 TL | Havale Dip Sınırı: 58.000 TL) ve 'POCO X8 Pro 256 GB' (Önerilen: 33.850,00 TL | Dip Sınır: 33.500 TL) ürünlerinde fiyatları güncelleyerek Akakçe/pazaryeri sıralamasında 1. sırayı geri alın.\n"
            "2. En ucuz satıcı olduğumuz 'Samsung Galaxy A26 256 GB' (Bizim: 22.900 TL, En Yakın Rakip: 23.390 TL) ve 'Apple iPad Mini 7 512 GB' ürünlerinde 1. sırayı kaybetmeden fiyat artışı yaparak ürün başına +350 TL ile +700 TL ek marj kazanın."
        )
        save_last_report(baseline_llm_report, report_data)
        print("✓ Cep-Hane Teknoloji yönetici özeti (data/last_report.json) hazırlandı.")
        print("\n" + "=" * 80)
        print("✅ [CEP-HANE DEMO HAZIR] 12 gerçek ürün ve 3 pazaryeri kanalı başarıyla kuruldu!")
        print("=" * 80)
    finally:
        session.close()


if __name__ == "__main__":
    reset_demo_state()

reset_demo_environment = reset_demo_state
