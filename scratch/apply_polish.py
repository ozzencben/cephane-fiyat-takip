from pathlib import Path

tmpl = Path(r"c:\Users\win\Desktop\cephane-fiyat-takip\src\fiyat_takip_sistemi\api\templates\index.html")
txt = tmpl.read_text(encoding="utf-8")

# 1. Container width
txt = txt.replace("max-width: 1560px;", "max-width: 1720px;")

# 2. My Price nowrap
old_my_price = """.my-price-val {
            font-family: var(--font-mono);
            font-weight: 800;
            font-size: 1.05rem;
            color: #0f172a;
        }"""
new_my_price = """.my-price-val {
            font-family: var(--font-mono);
            font-weight: 800;
            font-size: 1.05rem;
            color: #0f172a;
            white-space: nowrap;
        }"""
txt = txt.replace(old_my_price, new_my_price)

# 3. Market price nowrap
old_market_price = """.market-price {
            font-family: var(--font-mono);
            font-weight: 700;
            font-size: 0.975rem;
            color: #0f172a;
        }"""
new_market_price = """.market-price {
            font-family: var(--font-mono);
            font-weight: 700;
            font-size: 0.975rem;
            color: #0f172a;
            white-space: nowrap;
        }"""
txt = txt.replace(old_market_price, new_market_price)

# 4. Action widget min-width & nowrap
txt = txt.replace(".cell-action {\n            min-width: 220px;\n        }", ".cell-action {\n            min-width: 260px;\n        }")
txt = txt.replace(".cell-my-price {\n            min-width: 150px;\n        }", ".cell-my-price {\n            min-width: 170px;\n        }")

# 5. Header title for last column
txt = txt.replace("<th>Akıllı Karar &amp; Fiyat Önerisi</th>", "<th style=\"min-width:260px;\">Akıllı Karar &amp; Fiyat Önerisi</th>")

tmpl.write_text(txt, encoding="utf-8")
print("Applied polish fixes to index.html!")

