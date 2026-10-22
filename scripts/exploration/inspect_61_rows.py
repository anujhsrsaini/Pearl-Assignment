import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
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

init_null_with_disc = df[df['init_num'].isna() & (~df['discount'].isin(['', 'null']))].copy()
print(f"Total rows where initial_price is NULL but discount is populated: {len(init_null_with_disc)}")

print("\nDiscount breakdown for these 61 rows:")
print(init_null_with_disc['discount'].value_counts())

for idx, r in init_null_with_disc.iterrows():
    print(f"Row {idx:3d} | ASIN {r['asin']} | Final: {r['fin_num']} | Disc: {repr(r['discount'])}")
