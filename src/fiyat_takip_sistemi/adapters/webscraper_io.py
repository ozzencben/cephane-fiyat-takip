import sys
from typing import Any, Dict, List
from sqlalchemy.orm import Session

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from ..core.db import SessionLocal
from .base import save_validated_snapshots_to_db

HEPSIBURADA_LISTINGS: List[Dict[str, Any]] = [
    {"name": "Apple iPhone 15 128 GB (Apple Türkiye Garantili) Siyah", "price": 59490.00, "in_stock": True, "url": "https://www.hepsiburada.com/apple-iphone-15-128-gb-siyah"},
    {"name": "Apple iPhone 16e 128 GB (Apple Türkiye Garantili) Beyaz", "price": 52890.00, "in_stock": True, "url": "https://www.hepsiburada.com/apple-iphone-16e-128-gb-beyaz"},
    {"name": "Apple iPhone 16 Plus 128 GB (Apple Türkiye Garantili) Yeşil", "price": 83900.00, "in_stock": True, "url": "https://www.hepsiburada.com/apple-iphone-16-plus-128-gb-yesil"},
    {"name": "Samsung Galaxy A36 128 GB 8 GB RAM 5G (Samsung Türkiye Garantili) Gri", "price": 24950.00, "in_stock": True, "url": "https://www.hepsiburada.com/samsung-galaxy-a36-128-gb-gri"},
    {"name": "Samsung Galaxy A26 256 GB 8 GB RAM 5G (Samsung Türkiye Garantili) Beyaz", "price": 23790.00, "in_stock": True, "url": "https://www.hepsiburada.com/samsung-galaxy-a26-256-gb-beyaz"},
    {"name": "Samsung Galaxy A17 128 GB 6 GB RAM 5G (Samsung Türkiye Garantili) Gri", "price": 15390.00, "in_stock": True, "url": "https://www.hepsiburada.com/samsung-galaxy-a17-128-gb-gri"},
    {"name": "POCO X8 Pro 256 GB 8 GB RAM (Distribütör Garantili) Beyaz", "price": 34450.00, "in_stock": True, "url": "https://www.hepsiburada.com/poco-x8-pro-256-gb-beyaz"},
    {"name": "Apple iPad Mini 7 512 GB Wi-Fi + Cellular 8.3 inç Tablet Mavi", "price": 59950.00, "in_stock": True, "url": "https://www.hepsiburada.com/apple-ipad-mini-7-512-gb-mavi"},
    {"name": "Xiaomi Redmi Pad 2 64 GB 4 GB RAM 9.7 inç (Xiaomi Türkiye Garantili) Gri", "price": 7490.00, "in_stock": True, "url": "https://www.hepsiburada.com/xiaomi-redmi-pad-2-64-gb-gri"},
    {"name": "Samsung Watch 8 44 MM Akıllı Saat (Samsung Türkiye Garantili) Koyu Gri", "price": 12450.00, "in_stock": True, "url": "https://www.hepsiburada.com/samsung-watch-8-44mm-koyu-gri"},
    {"name": "Apple AirPods Pro 3 Bluetooth Kulaklık Beyaz", "price": 13790.00, "in_stock": True, "url": "https://www.hepsiburada.com/apple-airpods-pro-3-beyaz"},
    {"name": "Apple 20W USB-C Güç Adaptörü (Apple Türkiye Garantili) Beyaz", "price": 979.00, "in_stock": True, "url": "https://www.hepsiburada.com/apple-20w-usb-c-guc-adaptoru"},
]


class WebScraperIOAdapter:
    COMPETITOR_NAME = "Hepsiburada (En Ucuz Rakip)"
    BASE_URL = "https://www.hepsiburada.com"

    def fetch_products(self) -> List[Dict[str, Any]]:
        return list(HEPSIBURADA_LISTINGS)

    def close(self) -> None:
        pass


def save_snapshots_to_db(db: Session, products: List[Dict[str, Any]]) -> int:
    return save_validated_snapshots_to_db(
        db=db,
        competitor_name=WebScraperIOAdapter.COMPETITOR_NAME,
        base_url=WebScraperIOAdapter.BASE_URL,
        products=products,
    )


def main() -> None:
    adapter = WebScraperIOAdapter()
    session = SessionLocal()
    try:
        items = adapter.fetch_products()
        saved = save_snapshots_to_db(session, items)
        print(f"✓ {WebScraperIOAdapter.COMPETITOR_NAME}: {len(items)} ürün incelendi, {saved} yeni snapshot kaydedildi.")
    finally:
        session.close()
        adapter.close()


if __name__ == "__main__":
    main()
