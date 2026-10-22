import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

df = pd.read_csv('amazon-products.csv', dtype=str, keep_default_na=False)

rows = [5, 13, 15, 32, 57, 102, 203]
for r_idx in rows:
    row = df.iloc[r_idx]
    print(f"Row {r_idx} | ASIN: {row['asin']}")
    print(f"  Title: {row['title']}")
    print(f"  initial_price: {row['initial_price']}, final_price: {row['final_price']}, discount: {row['discount']}")
    print(f"  url: {row['url']}")
