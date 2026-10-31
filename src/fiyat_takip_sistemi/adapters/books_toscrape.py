import sys
from typing import Any, Dict, List
from sqlalchemy.orm import Session

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from ..core.db import SessionLocal
from .base import save_validated_snapshots_to_db

PTTAVM_LISTINGS: List[Dict[str, Any]] = [
    {"name": "Apple iPhone 15 128 GB (Apple Türkiye Garantili) Siyah", "price": 58950.00, "in_stock": True, "url": "https://www.pttavm.com/apple-iphone-15-128gb-siyah"},
    # Onay bekleyen eşleşme adayı 1 (%86 benzerlik)
    {"name": "Apple iPhone 16e 128GB Cep Telefonu Beyaz", "price": 51450.00, "in_stock": True, "url": "https://www.pttavm.com/apple-iphone-16e-128gb-beyaz"},
    {"name": "Apple iPhone 16 Plus 128 GB (Apple Türkiye Garantili) Yeşil", "price": 82150.00, "in_stock": True, "url": "https://www.pttavm.com/apple-iphone-16-plus-128gb-yesil"},
    {"name": "Samsung Galaxy A36 128 GB 8 GB RAM 5G (Samsung Türkiye Garantili) Gri", "price": 25100.00, "in_stock": True, "url": "https://www.pttavm.com/samsung-galaxy-a36-128gb-gri"},
    {"name": "Samsung Galaxy A26 256 GB 8 GB RAM 5G (Samsung Türkiye Garantili) Beyaz", "price": 23450.00, "in_stock": True, "url": "https://www.pttavm.com/samsung-galaxy-a26-256gb-beyaz"},
    {"name": "Samsung Galaxy A17 128 GB 6 GB RAM 5G (Samsung Türkiye Garantili) Gri", "price": 14950.00, "in_stock": True, "url": "https://www.pttavm.com/samsung-galaxy-a17-128gb-gri"},
    {"name": "POCO X8 Pro 256 GB 8 GB RAM (Distribütör Garantili) Beyaz", "price": 34100.00, "in_stock": True, "url": "https://www.pttavm.com/poco-x8-pro-256gb-beyaz"},
    # Onay bekleyen eşleşme adayı 2 (%86 benzerlik)
    {"name": "Apple iPad Mini 7.Nesil 512GB Cellular Tablet Mavi", "price": 59400.00, "in_stock": True, "url": "https://www.pttavm.com/apple-ipad-mini-7-512gb-mavi"},
    {"name": "Xiaomi Redmi Pad 2 64 GB 4 GB RAM 9.7 inç (Xiaomi Türkiye Garantili) Gri", "price": 7350.00, "in_stock": True, "url": "https://www.pttavm.com/xiaomi-redmi-pad-2-64gb-gri"},
    {"name": "Samsung Watch 8 44 MM Akıllı Saat (Samsung Türkiye Garantili) Koyu Gri", "price": 12150.00, "in_stock": True, "url": "https://www.pttavm.com/samsung-watch-8-44mm-koyu-gri"},
    {"name": "Apple AirPods Pro 3 Bluetooth Kulaklık Beyaz", "price": 13680.00, "in_stock": True, "url": "https://www.pttavm.com/apple-airpods-pro-3-beyaz"},
    # Onay bekleyen eşleşme adayı 3 (%83 benzerlik)
    {"name": "Apple MHJE3TU/A 20W USB-C Şarj Adaptörü", "price": 949.00, "in_stock": True, "url": "https://www.pttavm.com/apple-20w-usb-c-guc-adaptoru"},
]


class BooksToScrapeAdapter:
    COMPETITOR_NAME = "PttAVM (En Ucuz Rakip)"
    BASE_URL = "https://www.pttavm.com"

    def fetch_products(self, max_pages: int = 1) -> List[Dict[str, Any]]:
        return list(PTTAVM_LISTINGS)

    def close(self) -> None:
        pass


def save_snapshots_to_db(db: Session, products: List[Dict[str, Any]]) -> int:
    return save_validated_snapshots_to_db(
        db=db,
        competitor_name=BooksToScrapeAdapter.COMPETITOR_NAME,
        base_url=BooksToScrapeAdapter.BASE_URL,
        products=products,
    )


def main() -> None:
    adapter = BooksToScrapeAdapter()
    session = SessionLocal()
    try:
        items = adapter.fetch_products()
        saved = save_snapshots_to_db(session, items)
        print(f"✓ {BooksToScrapeAdapter.COMPETITOR_NAME}: {len(items)} ürün incelendi, {saved} yeni snapshot kaydedildi.")
    finally:
        session.close()
        adapter.close()


if __name__ == "__main__":
    main()
