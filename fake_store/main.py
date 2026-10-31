import json
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="N11 / Pazarama Elektronik Pazaryeri Simülasyonu (Port 8001)")


def get_prices_file() -> Path:
    candidates = [
        Path("data/prices.json"),
        Path(__file__).resolve().parent.parent / "data" / "prices.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    return Path("data/prices.json")


def load_products() -> List[Dict[str, Any]]:
    prices_file = get_prices_file()
    if not prices_file.exists():
        return []
    with open(prices_file, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/", response_class=HTMLResponse)
@app.get("/products", response_class=HTMLResponse)
def list_products() -> str:
    products = load_products()
    cards_html = ""
    for prod in products:
        pid = prod.get("id", 0)
        name = prod.get("name", "Bilinmeyen Ürün")
        price = prod.get("price", 0.0)
        in_stock = prod.get("in_stock", True)
        url = prod.get("url", f"http://localhost:8001/products/{pid}")

        stock_badge = (
            '<span class="product-stock in-stock" data-in-stock="true">Stokta Var</span>'
            if in_stock
            else '<span class="product-stock out-of-stock" data-in-stock="false">Tükendi</span>'
        )
        cards_html += f"""
        <div class="product-card" data-id="{pid}">
            <h3 class="product-name">{name}</h3>
            <p class="product-price" data-price="{price:.2f}">{price:,.2f} TL</p>
            {stock_badge}
            <a class="product-link" href="{url}">Pazaryeri İlanını İncele</a>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Pazaryeri Elektronik Vitrini — Canlı Fiyat Simülasyonu</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f9; margin: 0; padding: 30px; color: #1e293b; }}
        .header {{ max-width: 1180px; margin: 0 auto 24px auto; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 14px; }}
        .header h1 {{ margin: 0; font-size: 26px; color: #0f172a; }}
        .header p {{ margin: 4px 0 0 0; color: #64748b; font-size: 14px; }}
        .badge-count {{ background: #e0e7ff; color: #3730a3; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 14px; }}
        .grid {{ max-width: 1180px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(265px, 1fr)); gap: 18px; }}
        .product-card {{ background: #ffffff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; display: flex; flex-direction: column; justify-content: space-between; }}
        .product-name {{ font-size: 15px; margin: 0 0 12px 0; color: #1e293b; line-height: 1.4; min-height: 42px; }}
        .product-price {{ font-size: 22px; font-weight: 700; color: #059669; margin: 0 0 10px 0; }}
        .product-stock {{ display: inline-block; width: fit-content; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; margin-bottom: 14px; }}
        .in-stock {{ background: #dcfce7; color: #166534; }}
        .out-of-stock {{ background: #fee2e2; color: #991b1b; }}
        .product-link {{ display: block; text-align: center; background: #2563eb; color: #fff; text-decoration: none; padding: 9px 12px; border-radius: 8px; font-weight: 600; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>📱 Pazaryeri Elektronik & Cep Telefonu Vitrini</h1>
            <p>N11 / Pazarama Canlı Rakip Fiyat Simülasyon Mağazası (Port 8001)</p>
        </div>
        <span class="badge-count">{len(products)} Elektronik Ürün</span>
    </div>
    <div class="grid">
        {cards_html}
    </div>
</body>
</html>"""
