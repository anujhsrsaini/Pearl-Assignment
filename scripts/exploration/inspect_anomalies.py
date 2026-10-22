import pandas as pd
import json

df = pd.read_csv('amazon-products.csv', dtype=str, keep_default_na=False)

def clean_num(val):
    if not val or val.strip().lower() == 'null':
        return None
    import re
    c = re.sub(r'[\"\'$,₹\s]', '', str(val))
    try:
        return float(c)
    except:
        return None

df['init_f'] = df['initial_price'].apply(clean_num)
df['fin_f'] = df['final_price'].apply(clean_num)

# Let's check the 3 rows where final_price is null!
print("--- Rows where final_price is null ---")
fin_null = df[df['fin_f'].isna()]
for idx, row in fin_null.iterrows():
    print(f"Row {idx} | ASIN: {row['asin']} | Title: {row['title'][:40]} | Init: {row['initial_price']} | Fin: {row['final_price']} | Disc: {row['discount']} | Buybox: {row['buybox_prices']}")

# Let's check row 992 (inverted price)
print("\n--- Row 992 (Inverted price) ---")
r992 = df.iloc[992]
print(f"ASIN: {r992['asin']} | Title: {r992['title']} | Init: {r992['initial_price']} | Fin: {r992['final_price']} | Disc: {r992['discount']} | Buybox: {r992['buybox_prices']}")
