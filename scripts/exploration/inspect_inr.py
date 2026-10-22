import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import json

df = pd.read_csv('amazon-products.csv', dtype=str, keep_default_na=False)

inr_rows = df[df['currency'] == 'INR']
print(f"Total INR rows: {len(inr_rows)}")
for idx, r in inr_rows.head(10).iterrows():
    print(f"Row {idx:3d} ASIN {r['asin']} | Init: {r['initial_price']:10s} | Fin: {r['final_price']:10s} | Disc: {repr(r['discount']):20s}")
