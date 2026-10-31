import json
import sys
from pathlib import Path
from typing import Any, Dict, List
import httpx
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from ..core.db import SessionLocal
from .base import parse_and_validate_price, save_validated_snapshots_to_db


class FakeStoreAdapter:
    COMPETITOR_NAME = "N11 / Pazarama (En Ucuz Rakip)"
    BASE_URL = "http://localhost:8001"

    def __init__(self) -> None:
        self.client = httpx.Client(
            headers={"User-Agent": "FiyatTakipBot/1.0 (Cephane Demo)"},
            timeout=10.0,
            follow_redirects=True,
        )

    def fetch_products(self) -> List[Dict[str, Any]]:
        url = f"{self.BASE_URL}/products"
        try:
            response = self.client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select("div.product-card")
            results: List[Dict[str, Any]] = []
            for card in cards:
                name_el = card.select_one("h3.product-name")
                price_el = card.select_one("p.product-price")
                stock_el = card.select_one("span.product-stock")
                link_el = card.select_one("a.product-link")
                if not name_el or not price_el:
                    continue
                name = name_el.get_text(strip=True)
                raw_price = price_el.get("data-price") or price_el.get_text(strip=True)
                price = parse_and_validate_price(raw_price, product_name=name, source=self.COMPETITOR_NAME)
                if price is None:
                    continue
                in_stock = True
                if stock_el:
                    stock_attr = stock_el.get("data-in-stock")
                    if stock_attr is not None:
                        in_stock = stock_attr.lower() == "true"
                    else:
                        in_stock = "stokta var" in stock_el.get_text(strip=True).lower()
                prod_url = link_el.get("href") if link_el else url
                results.append({"name": name, "price": price, "in_stock": in_stock, "url": str(prod_url)})
            if results:
                return results
        except Exception:
            pass

        # Sunucu kapalıysa doğrudan data/prices.json dosyasından oku
        prices_path = Path(__file__).resolve().parents[3] / "data" / "prices.json"
        if prices_path.exists():
            data = json.loads(prices_path.read_text(encoding="utf-8"))
            return [
                {
                    "name": item["name"],
                    "price": float(item["price"]),
                    "in_stock": bool(item.get("in_stock", True)),
                    "url": item.get("url", f"{self.BASE_URL}/products/{item.get('id', 1)}"),
                }
                for item in data
            ]
        return []

    def close(self) -> None:
        self.client.close()


def save_snapshots_to_db(db: Session, products: List[Dict[str, Any]]) -> int:
    return save_validated_snapshots_to_db(
        db=db,
        competitor_name=FakeStoreAdapter.COMPETITOR_NAME,
        base_url=FakeStoreAdapter.BASE_URL,
        products=products,
    )


def main() -> None:
    adapter = FakeStoreAdapter()
    session = SessionLocal()
    try:
        items = adapter.fetch_products()
        saved = save_snapshots_to_db(session, items)
        print(f"✓ {FakeStoreAdapter.COMPETITOR_NAME}: {len(items)} ürün incelendi, {saved} yeni snapshot kaydedildi.")
    finally:
        session.close()
        adapter.close()


if __name__ == "__main__":
    main()
