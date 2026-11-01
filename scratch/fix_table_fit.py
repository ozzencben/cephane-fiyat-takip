from pathlib import Path

tmpl = Path(r"c:\Users\win\Desktop\cephane-fiyat-takip\src\fiyat_takip_sistemi\api\templates\index.html")
txt = tmpl.read_text(encoding="utf-8")

# Column adjustments for perfect 1440px desktop fit
txt = txt.replace(".cell-product {\n            min-width: 280px;\n            max-width: 320px;\n        }", ".cell-product {\n            min-width: 240px;\n        }")
txt = txt.replace(".cell-my-price {\n            min-width: 170px;\n        }", ".cell-my-price {\n            min-width: 135px;\n        }")
txt = txt.replace(".cell-marketplace {\n            min-width: 175px;\n        }", ".cell-marketplace {\n            min-width: 155px;\n        }")
txt = txt.replace(".cell-diff {\n            min-width: 140px;\n        }", ".cell-diff {\n            min-width: 130px;\n        }")
txt = txt.replace(".cell-action {\n            min-width: 260px;\n        }", ".cell-action {\n            min-width: 215px;\n        }")
txt = txt.replace("<th style=\"min-width:260px;\">Akıllı Karar &amp; Fiyat Önerisi</th>", "<th>Akıllı Karar &amp; Fiyat Önerisi</th>")

# Adjust padding
txt = txt.replace("padding: 0.85rem 1rem;", "padding: 0.75rem 0.65rem;")
txt = txt.replace("padding: 1.1rem 1rem;", "padding: 0.75rem 0.65rem;")

# Table card padding / container padding
txt = txt.replace("padding: 1.5rem 1.75rem 4rem 1.75rem;", "padding: 1.25rem 1.25rem 3.5rem 1.25rem;")

tmpl.write_text(txt, encoding="utf-8")
print("Tuned table fit for zero overflow!")

