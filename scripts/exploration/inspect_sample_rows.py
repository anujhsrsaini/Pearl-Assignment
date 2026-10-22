import pandas as pd
import json

df = pd.read_csv('amazon-products.csv', dtype=str, keep_default_na=False)

rows_to_check = [3, 5, 13, 15, 20, 32, 57, 992, 102, 203]
for idx in rows_to_check:
    row = df.iloc[idx]
    print(f"--- Row {idx} (ASIN: {row['asin']}) ---")
    print(f"initial_price: {row['initial_price']}")
    print(f"final_price:   {row['final_price']}")
    print(f"discount:      {repr(row['discount'])}")
    print(f"buybox_prices: {row['buybox_prices']}")
