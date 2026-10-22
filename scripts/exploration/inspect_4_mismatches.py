import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

df = pd.read_csv('amazon-products.csv', dtype=str, keep_default_na=False)

for r_idx in [159, 222, 460, 642]:
    r = df.iloc[r_idx]
    print(f"--- Row {r_idx} (ASIN: {r['asin']}) ---")
    print(f"Title: {r['title']}")
    print(f"initial_price: {r['initial_price']}, final_price: {r['final_price']}, discount: {r['discount']}, currency: {r['currency']}")
    print(f"buybox_prices: {r['buybox_prices']}")
