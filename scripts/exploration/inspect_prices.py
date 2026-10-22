import pandas as pd
import json
import re

df = pd.read_csv('amazon-products.csv', dtype=str, keep_default_na=False)

init_null = df[df['initial_price'].isin(['', 'null'])]
print(f"Total initial_price null: {len(init_null)}")
print(f"  discount is empty/null: {len(init_null[init_null['discount'].isin(['', 'null'])])}")
print(f"  discount is populated: {len(init_null[~init_null['discount'].isin(['', 'null'])])}")

print("\n--- Rows where initial_price is null AND discount is empty/null (125 rows) ---")
print("What does this mean? Product is sold at standard retail price without discount?")
sample_no_disc = init_null[init_null['discount'].isin(['', 'null'])][['asin', 'final_price', 'currency', 'buybox_prices']].head(5)
for idx, row in sample_no_disc.iterrows():
    print(f"ASIN: {row['asin']} | Final Price: {row['final_price']} | Currency: {row['currency']} | Buybox: {row['buybox_prices'][:80]}")

print("\n--- Rows where initial_price is null BUT discount IS populated (61 rows) ---")
sample_with_disc = init_null[~init_null['discount'].isin(['', 'null'])][['asin', 'final_price', 'discount', 'currency', 'buybox_prices']].head(10)
for idx, row in sample_with_disc.iterrows():
    print(f"ASIN: {row['asin']} | Final: {row['final_price']} | Discount: {repr(row['discount'])} | Buybox: {row['buybox_prices'][:80]}")
