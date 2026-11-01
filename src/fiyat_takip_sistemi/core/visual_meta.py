# -*- coding: utf-8 -*-
from typing import Any, Dict

# Elektronik ǬrǬnlerine zel grsel kimlik ve ikonlar (SVG)
DEVICE_SVGS = {
    "phone_apple": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="3"/><path d="M12 18h.01"/></svg>""",
    "phone_android": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1e40af" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2.5"/><circle cx="12" cy="18" r="0.75" fill="currentColor"/></svg>""",
    "phone_poco": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ca8a04" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2.5"/><path d="m9 10 3 4 3-4"/></svg>""",
    "tablet": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4338ca" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="20" x="4" y="2" rx="2"/><circle cx="12" cy="18" r="0.75" fill="currentColor"/></svg>""",
    "watch": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#047857" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="12" height="13" x="6" y="5.5" rx="3"/><path d="M9 2h6v3.5H9zM9 18.5h6V22H9z"/><circle cx="12" cy="12" r="1.5"/></svg>""",
    "audio": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#6d28d9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/></svg>""",
    "charger": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#b45309" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="12" height="12" x="6" y="8" rx="2"/><path d="M9 2v6M15 2v6M12 14v4"/></svg>""",
}

PRODUCT_VISUALS: Dict[str, Dict[str, Any]] = {
    "CPH-001": {
        "brand": "Apple",
        "brand_badge": "apple-badge",
        "category": "Cep Telefonu",
        "svg_icon": DEVICE_SVGS["phone_apple"],
        "bg_color": "#f1f5f9",
        "short_title": "iPhone 15 128 GB",
        "specs": ["128 GB", "Siyah", "Apple TR Garantili"],
    },
    "CPH-002": {
        "brand": "Apple",
        "brand_badge": "apple-badge",
        "category": "Cep Telefonu",
        "svg_icon": DEVICE_SVGS["phone_apple"],
        "bg_color": "#f1f5f9",
        "short_title": "iPhone 16e 128 GB",
        "specs": ["128 GB", "Beyaz", "Apple TR Garantili"],
    },
    "CPH-003": {
        "brand": "Apple",
        "brand_badge": "apple-badge",
        "category": "Cep Telefonu",
        "svg_icon": DEVICE_SVGS["phone_apple"],
        "bg_color": "#ecfdf5",
        "short_title": "iPhone 16 Plus 128 GB",
        "specs": ["128 GB", "Yeşil", "Apple TR Garantili"],
    },
    "CPH-004": {
        "brand": "Samsung",
        "brand_badge": "samsung-badge",
        "category": "Cep Telefonu",
        "svg_icon": DEVICE_SVGS["phone_android"],
        "bg_color": "#eff6ff",
        "short_title": "Galaxy A36 128 GB 5G",
        "specs": ["128 GB", "8 GB RAM", "Gri", "Samsung TR"],
    },
    "CPH-005": {
        "brand": "Samsung",
        "brand_badge": "samsung-badge",
        "category": "Cep Telefonu",
        "svg_icon": DEVICE_SVGS["phone_android"],
        "bg_color": "#eff6ff",
        "short_title": "Galaxy A26 256 GB 5G",
        "specs": ["256 GB", "8 GB RAM", "Beyaz", "Samsung TR"],
    },
    "CPH-006": {
        "brand": "Samsung",
        "brand_badge": "samsung-badge",
        "category": "Cep Telefonu",
        "svg_icon": DEVICE_SVGS["phone_android"],
        "bg_color": "#eff6ff",
        "short_title": "Galaxy A17 128 GB 5G",
        "specs": ["128 GB", "6 GB RAM", "Gri", "Samsung TR"],
    },
    "CPH-007": {
        "brand": "POCO",
        "brand_badge": "poco-badge",
        "category": "Cep Telefonu",
        "svg_icon": DEVICE_SVGS["phone_poco"],
        "bg_color": "#fefce8",
        "short_title": "POCO X8 Pro 256 GB",
        "specs": ["256 GB", "8 GB RAM", "Beyaz", "Distribütör Garantili"],
    },
    "CPH-008": {
        "brand": "Apple",
        "brand_badge": "apple-badge",
        "category": "Tablet",
        "svg_icon": DEVICE_SVGS["tablet"],
        "bg_color": "#f5f3ff",
        "short_title": "iPad Mini 7 512 GB Cellular",
        "specs": ["512 GB", "8.3 inç", "Mavi", "Apple TR"],
    },
    "CPH-009": {
        "brand": "Xiaomi",
        "brand_badge": "xiaomi-badge",
        "category": "Tablet",
        "svg_icon": DEVICE_SVGS["tablet"],
        "bg_color": "#fff7ed",
        "short_title": "Redmi Pad 2 64 GB",
        "specs": ["64 GB", "4 GB RAM", "9.7 inç", "Xiaomi TR"],
    },
    "CPH-010": {
        "brand": "Samsung",
        "brand_badge": "samsung-badge",
        "category": "Akıllı Saat",
        "svg_icon": DEVICE_SVGS["watch"],
        "bg_color": "#f0fdf4",
        "short_title": "Watch 8 44 MM",
        "specs": ["44 MM", "Koyu Gri", "Samsung TR Garantili"],
    },
    "CPH-011": {
        "brand": "Apple",
        "brand_badge": "apple-badge",
        "category": "Kulaklık",
        "svg_icon": DEVICE_SVGS["audio"],
        "bg_color": "#faf5ff",
        "short_title": "AirPods Pro 3",
        "specs": ["Bluetooth", "Beyaz", "Apple Türkiye"],
    },
    "CPH-012": {
        "brand": "Apple",
        "brand_badge": "apple-badge",
        "category": "Aksesuar",
        "svg_icon": DEVICE_SVGS["charger"],
        "bg_color": "#fffbeb",
        "short_title": "20W USB-C Adaptör",
        "specs": ["20W Hızlı Şarj", "USB-C", "Apple TR"],
    },
}

def get_product_visual(sku: str) -> Dict[str, Any]:
    default_vis = {
        "brand": "Elektronik",
        "brand_badge": "apple-badge",
        "category": "Cihaz",
        "svg_icon": DEVICE_SVGS["phone_apple"],
        "bg_color": "#f8fafc",
        "short_title": sku,
        "specs": ["Resmi Garantili"],
    }
    return PRODUCT_VISUALS.get(sku, default_vis)

