import sys
sys.stdout.reconfigure(encoding='utf-8')
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

df['init_num'] = df['initial_price'].apply(clean_num)
df['fin_num'] = df['final_price'].apply(clean_num)

print("=== DEEP DIVE: DISCOUNTS WHEN init_num IS POPULATED ===")
# Check Bare Integer discounts: do they represent percentage or dollars?
bare_ints = df[df['discount'].str.match(r'^\d+$')]
print(f"Total bare integer discounts: {len(bare_ints)}")
matches_perc = 0
matches_diff = 0
for idx, r in bare_ints.iterrows():
    val = float(r['discount'])
    ip = r['init_num']
    fp = r['fin_num']
    if ip and fp and ip > fp:
        pct = round((ip - fp) / ip * 100)
        diff = round(ip - fp, 2)
        if abs(pct - val) <= 1:
            matches_perc += 1
        elif abs(diff - val) <= 0.05:
            matches_diff += 1

print(f"  Bare integers matching calculated %: {matches_perc} / {len(bare_ints)}")
print(f"  Bare integers matching price difference ($): {matches_diff} / {len(bare_ints)}")

print("\n=== DEEP DIVE: CURRENCY ONLY DISCOUNTS (e.g. $7.00) ===")
curr_only = df[df['discount'].str.contains(r'^[\$₹]\d+(\.\d+)?$')]
print(f"Total currency-only discounts: {len(curr_only)}")
matches_curr_diff = 0
init_is_null_count = 0
for idx, r in curr_only.iterrows():
    c_val = float(re.sub(r'[^\d.]', '', r['discount']))
    ip = r['init_num']
    fp = r['fin_num']
    if ip is None:
        init_is_null_count += 1
    elif fp is not None and ip > fp:
        diff = round(ip - fp, 2)
        if abs(diff - c_val) <= 0.05:
            matches_curr_diff += 1
print(f"  Currency-only where initial_price is NULL: {init_is_null_count}")
print(f"  Currency-only matching (init - fin): {matches_curr_diff}")
print("  Sample currency-only rows where initial_price is NOT null:")
sample_co = curr_only[curr_only['init_num'].notna()][['asin', 'initial_price', 'final_price', 'discount']].head(5)
print(sample_co)

print("\n  Sample currency-only rows where initial_price IS null:")
sample_co_null = curr_only[curr_only['init_num'].isna()][['asin', 'initial_price', 'final_price', 'discount']].head(5)
print(sample_co_null)
