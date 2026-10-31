from typing import Any, Dict

# Her ürün (SKU) ve pazaryeri rolü (rakip_a=PttAVM, rakip_b=Hepsiburada, rakip_c=N11/Pazarama)
# için gerçekçi elektronik satıcı mağaza profilleri, mağaza puanları ve stok bilgileri.
SELLER_PROFILES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "CPH-001": {
        "rakip_a": {"satici": "Bittibitti", "puan": 9.6, "stok_notu": "Son 3 stok", "kargo": "Ücretsiz Kargo"},
        "rakip_b": {"satici": "Hepsiburada", "puan": 9.9, "stok_notu": "Stokta (10+)", "kargo": "Yarın Kapında"},
        "rakip_c": {"satici": "TeknoMerkez", "puan": 9.4, "stok_notu": "Son 4 stok", "kargo": "Ücretsiz Kargo"},
    },
    "CPH-002": {
        "rakip_a": {"satici": "CepDünyası", "puan": 9.3, "stok_notu": "Son 2 stok", "kargo": "Ücretsiz Kargo"},
        "rakip_b": {"satici": "GpnTeknoloji", "puan": 9.8, "stok_notu": "Stokta (10+)", "kargo": "Hızlı Teslimat"},
        "rakip_c": {"satici": "Elmacık", "puan": 9.7, "stok_notu": "Son 5 stok", "kargo": "Ücretsiz Kargo"},
    },
    "CPH-003": {
        "rakip_a": {"satici": "Teknohanem", "puan": 9.5, "stok_notu": "Son 2 stok", "kargo": "Ücretsiz Kargo"},
        "rakip_b": {"satici": "MediaMarkt", "puan": 9.8, "stok_notu": "Stokta (10+)", "kargo": "Ücretsiz Kargo"},
        "rakip_c": {"satici": "VizyonTekno", "puan": 9.4, "stok_notu": "Son 3 stok", "kargo": "Bugün Kargoda"},
    },
    "CPH-004": {
        "rakip_a": {"satici": "NetSipariş", "puan": 9.4, "stok_notu": "Son 4 stok", "kargo": "Ücretsiz Kargo"},
        "rakip_b": {"satici": "Hepsiburada", "puan": 9.9, "stok_notu": "Stokta (10+)", "kargo": "Yarın Kapında"},
        "rakip_c": {"satici": "TrendCep", "puan": 9.5, "stok_notu": "Stokta (5+)", "kargo": "Ücretsiz Kargo"},
    },
    "CPH-005": {
        "rakip_a": {"satici": "AkıllıFiyat", "puan": 9.2, "stok_notu": "Son 5 stok", "kargo": "Ücretsiz Kargo"},
        "rakip_b": {"satici": "TeknoPark", "puan": 9.6, "stok_notu": "Stokta (10+)", "kargo": "Ücretsiz Kargo"},
        "rakip_c": {"satici": "CepEkspres", "puan": 9.3, "stok_notu": "Son 3 stok", "kargo": "Bugün Kargoda"},
    },
    "CPH-006": {
        "rakip_a": {"satici": "FırsatReyonu", "puan": 9.1, "stok_notu": "Son 1 stok", "kargo": "Ücretsiz Kargo"},
        "rakip_b": {"satici": "GpnTeknoloji", "puan": 9.8, "stok_notu": "Stokta (10+)", "kargo": "Hızlı Teslimat"},
        "rakip_c": {"satici": "TeknoMerkez", "puan": 9.4, "stok_notu": "Son 4 stok", "kargo": "Ücretsiz Kargo"},
    },
    "CPH-007": {
        "rakip_a": {"satici": "Bittibitti", "puan": 9.6, "stok_notu": "Son 3 stok", "kargo": "Ücretsiz Kargo"},
        "rakip_b": {"satici": "MiekoTeknoloji", "puan": 9.7, "stok_notu": "Stokta (10+)", "kargo": "Bugün Kargoda"},
        "rakip_c": {"satici": "VizyonTekno", "puan": 9.4, "stok_notu": "Son 2 stok", "kargo": "Ücretsiz Kargo"},
    },
    "CPH-008": {
        "rakip_a": {"satici": "Elmacık", "puan": 9.7, "stok_notu": "Son 2 stok", "kargo": "Ücretsiz Kargo"},
        "rakip_b": {"satici": "Hepsiburada", "puan": 9.9, "stok_notu": "Stokta (5+)", "kargo": "Yarın Kapında"},
        "rakip_c": {"satici": "TeknoPark", "puan": 9.6, "stok_notu": "Tükendi", "kargo": "Stok Yok"},
    },
    "CPH-009": {
        "rakip_a": {"satici": "TabletMerkezi", "puan": 9.4, "stok_notu": "Stokta (5+)", "kargo": "Ücretsiz Kargo"},
        "rakip_b": {"satici": "MediaMarkt", "puan": 9.8, "stok_notu": "Stokta (10+)", "kargo": "Ücretsiz Kargo"},
        "rakip_c": {"satici": "NetSipariş", "puan": 9.4, "stok_notu": "Son 3 stok", "kargo": "Bugün Kargoda"},
    },
    "CPH-010": {
        "rakip_a": {"satici": "SaatTekno", "puan": 9.5, "stok_notu": "Son 2 stok", "kargo": "Ücretsiz Kargo"},
        "rakip_b": {"satici": "Hepsiburada", "puan": 9.9, "stok_notu": "Stokta (10+)", "kargo": "Yarın Kapında"},
        "rakip_c": {"satici": "TrendCep", "puan": 9.5, "stok_notu": "Son 4 stok", "kargo": "Ücretsiz Kargo"},
    },
    "CPH-011": {
        "rakip_a": {"satici": "Bittibitti", "puan": 9.6, "stok_notu": "Son 4 stok", "kargo": "Ücretsiz Kargo"},
        "rakip_b": {"satici": "Hepsiburada", "puan": 9.9, "stok_notu": "Stokta (10+)", "kargo": "Yarın Kapında"},
        "rakip_c": {"satici": "Elmacık", "puan": 9.7, "stok_notu": "Stokta (10+)", "kargo": "Ücretsiz Kargo"},
    },
    "CPH-012": {
        "rakip_a": {"satici": "AksesuarHane", "puan": 9.3, "stok_notu": "Stokta (10+)", "kargo": "Hızlı Kargo"},
        "rakip_b": {"satici": "GpnTeknoloji", "puan": 9.8, "stok_notu": "Stokta (10+)", "kargo": "Yarın Kapında"},
        "rakip_c": {"satici": "TeknoMerkez", "puan": 9.4, "stok_notu": "Son 5 stok", "kargo": "Ücretsiz Kargo"},
    },
}


def get_competitor_role_from_name(comp_name: str) -> str:
    ad_lower = (comp_name or "").lower()
    if "pttavm" in ad_lower or "rakip a" in ad_lower or "bookstoscrape" in ad_lower:
        return "rakip_a"
    if "hepsiburada" in ad_lower or "rakip b" in ad_lower or "webscraper" in ad_lower:
        return "rakip_b"
    return "rakip_c"


def get_marketplace_short_name(comp_name: str) -> str:
    role = get_competitor_role_from_name(comp_name)
    if role == "rakip_a":
        return "PttAVM"
    if role == "rakip_b":
        return "Hepsiburada"
    return "N11 / Pazarama"


def get_seller_profile(sku: str, comp_name: str, stokta: bool = True) -> Dict[str, Any]:
    role = get_competitor_role_from_name(comp_name)
    channel_short = get_marketplace_short_name(comp_name)
    default_profile = {"satici": "TeknoMağaza", "puan": 9.5, "stok_notu": "Stokta", "kargo": "Ücretsiz Kargo"}
    prof = dict(SELLER_PROFILES.get(sku, {}).get(role, default_profile))
    if not stokta:
        prof["stok_notu"] = "Tükendi"
    prof["kanal"] = channel_short
    prof["etiket"] = f"{channel_short} / {prof['satici']} (★{prof['puan']})"
    return prof
