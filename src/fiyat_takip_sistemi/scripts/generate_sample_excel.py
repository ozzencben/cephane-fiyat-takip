from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

# Cep-Hane Teknoloji (https://cephaneteknoloji.com/katalog) üzerinden alınan 12 gerçek ürün
# fiyat = Sitedeki Kredi Kartı Satış Fiyatı (TL)
# dip_fiyat (maliyet * (1 + min_marj/100)) = Sitedeki Havale / EFT (%3 İndirimli) Dip Fiyatı (TL)
CEPHANE_PRODUCTS = [
    {
        "sku": "CPH-001",
        "urun_adi": "Apple iPhone 15 128 GB (Apple Türkiye Garantili) Siyah",
        "fiyat": 59800.00,
        "havale_dip": 58000.00,
        "min_marj_yuzde": 10,
    },
    {
        "sku": "CPH-002",
        "urun_adi": "Apple iPhone 16e 128 GB (Apple Türkiye Garantili) Beyaz",
        "fiyat": 53200.00,
        "havale_dip": 51600.00,
        "min_marj_yuzde": 10,
    },
    {
        "sku": "CPH-003",
        "urun_adi": "Apple iPhone 16 Plus 128 GB (Apple Türkiye Garantili) Yeşil",
        "fiyat": 83600.00,
        "havale_dip": 81000.00,
        "min_marj_yuzde": 10,
    },
    {
        "sku": "CPH-004",
        "urun_adi": "Samsung Galaxy A36 128 GB 8 GB RAM 5G (Samsung Türkiye Garantili) Gri",
        "fiyat": 25400.00,
        "havale_dip": 24600.00,
        "min_marj_yuzde": 10,
    },
    {
        "sku": "CPH-005",
        "urun_adi": "Samsung Galaxy A26 256 GB 8 GB RAM 5G (Samsung Türkiye Garantili) Beyaz",
        "fiyat": 22900.00,
        "havale_dip": 22200.00,
        "min_marj_yuzde": 10,
    },
    {
        "sku": "CPH-006",
        "urun_adi": "Samsung Galaxy A17 128 GB 6 GB RAM 5G (Samsung Türkiye Garantili) Gri",
        "fiyat": 15500.00,
        "havale_dip": 15000.00,
        "min_marj_yuzde": 10,
    },
    {
        "sku": "CPH-007",
        "urun_adi": "POCO X8 Pro 256 GB 8 GB RAM (Distribütör Garantili) Beyaz",
        "fiyat": 34600.00,
        "havale_dip": 33500.00,
        "min_marj_yuzde": 10,
    },
    {
        "sku": "CPH-008",
        "urun_adi": "Apple iPad Mini 7 512 GB Wi-Fi + Cellular 8.3 inç Tablet Mavi",
        "fiyat": 58300.00,
        "havale_dip": 56500.00,
        "min_marj_yuzde": 10,
    },
    {
        "sku": "CPH-009",
        "urun_adi": "Xiaomi Redmi Pad 2 64 GB 4 GB RAM 9.7 inç (Xiaomi Türkiye Garantili) Gri",
        "fiyat": 7100.00,
        "havale_dip": 6800.00,
        "min_marj_yuzde": 12,
    },
    {
        "sku": "CPH-010",
        "urun_adi": "Samsung Watch 8 44 MM Akıllı Saat (Samsung Türkiye Garantili) Koyu Gri",
        "fiyat": 12500.00,
        "havale_dip": 12100.00,
        "min_marj_yuzde": 12,
    },
    {
        "sku": "CPH-011",
        "urun_adi": "Apple AirPods Pro 3 Bluetooth Kulaklık Beyaz",
        "fiyat": 13900.00,
        "havale_dip": 13400.00,
        "min_marj_yuzde": 12,
    },
    {
        "sku": "CPH-012",
        "urun_adi": "Apple 20W USB-C Güç Adaptörü (Apple Türkiye Garantili) Beyaz",
        "fiyat": 1000.00,
        "havale_dip": 875.00,
        "min_marj_yuzde": 15,
    },
]


def create_excel(file_path: str = "data/urunlerim.xlsx") -> None:
    path = Path(file_path)
    if not path.is_absolute():
        project_root = Path(__file__).resolve().parents[3]
        path = project_root / file_path
    path.parent.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cephane_Urunler"

    headers = ["sku", "urun_adi", "fiyat", "maliyet", "min_marj_yuzde"]
    ws.append(headers)

    header_fill = PatternFill(start_color="1E40AF", end_color="1E40AF", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    for item in CEPHANE_PRODUCTS:
        marj = item["min_marj_yuzde"]
        # maliyet * (1 + marj/100) = havale_dip olacak şekilde birim maliyet
        maliyet = round(item["havale_dip"] / (1.0 + marj / 100.0), 2)
        ws.append([
            item["sku"],
            item["urun_adi"],
            item["fiyat"],
            maliyet,
            marj,
        ])

    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 68
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 18

    wb.save(path)
    print(f"✓ Cep-Hane Teknoloji'nin {len(CEPHANE_PRODUCTS)} gerçek ürünü '{path}' dosyasına kaydedildi.")


if __name__ == "__main__":
    create_excel()
