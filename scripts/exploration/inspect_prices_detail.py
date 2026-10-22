import pandas as pd
import json
import re

df = pd.read_csv('amazon-products.csv', dtype=str, keep_default_na=False)

def clean_num(val):
    if not val or val.strip().lower() == 'null':
        return None
    c = re.sub(r'[\"\'$,₹\s]', '', str(val))
    try:
        return float(c)
    except:
        return None

df['init_f'] = df['initial_price'].apply(clean_num)
df['fin_f'] = df['final_price'].apply(clean_num)

print("--- Categorization of all 1,000 rows by (init_f, fin_f) status ---")
init_valid = df['init_f'].notna()
fin_valid = df['fin_f'].notna()
has_disc = ~df['discount'].isin(['', 'null'])

print(f"1. Both initial & final populated: {(init_valid & fin_valid).sum()}")
print(f"2. Final populated, Initial NULL: {(~init_valid & fin_valid).sum()}")
print(f"3. Initial populated, Final NULL: {(init_valid & ~fin_valid).sum()}")
print(f"4. Both Initial & Final NULL: {(~init_valid & ~fin_valid).sum()}")

print("\n--- In group 1 (Both populated, 811 rows): ---")
g1 = df[init_valid & fin_valid].copy()
g1['diff'] = g1['init_f'] - g1['fin_f']
print(f"  init > fin (Standard discount): {(g1['diff'] > 0.001).sum()}")
print(f"  init == fin (Identical prices): {(g1['diff'].abs() <= 0.001).sum()}")
print(f"  init < fin (Inverted prices): {(g1['diff'] < -0.001).sum()}")

print("\n--- In group 1 where init == fin (87 rows): ---")
print(f"  discount is populated: {(g1[g1['diff'].abs() <= 0.001]['discount'].str.strip() != '').sum()}")
print(f"  sample of discounts in init == fin:")
print(g1[g1['diff'].abs() <= 0.001][['asin', 'init_f', 'fin_f', 'discount', 'buybox_prices']].head(10))

print("\n--- In group 1 where init < fin (Inverted, 1 row): ---")
print(g1[g1['diff'] < -0.001][['asin', 'init_f', 'fin_f', 'discount', 'buybox_prices']])

print("\n--- In group 1 where init > fin (Standard discount, 723 rows): ---")
print(f"  discount is populated: {(g1[g1['diff'] > 0.001]['discount'].str.strip() != '').sum()}")
print(f"  discount is empty: {(g1[g1['diff'] > 0.001]['discount'].str.strip() == '').sum()}")
