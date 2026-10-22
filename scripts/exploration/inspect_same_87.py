import sys
sys.stdout.reconfigure(encoding='utf-8')
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

df['init_num'] = df['initial_price'].apply(clean_num)
df['fin_num'] = df['final_price'].apply(clean_num)

same = df[(df['init_num'] == df['fin_num']) & (~df['discount'].isin(['', 'null']))]

print(f"Total same rows: {len(same)}")
for idx, r in same.head(15).iterrows():
    print(f"Row {idx} ASIN {r['asin']} | Price: {r['final_price']} | Disc: {r['discount']} | Buybox: {r['buybox_prices']}")
