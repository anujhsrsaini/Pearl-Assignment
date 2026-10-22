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

same_no_disc = df[(df['init_num'] == df['fin_num']) & (df['discount'].isin(['', 'null']))]
print(f"Count of rows where init == fin AND discount is empty: {len(same_no_disc)}")
for idx, r in same_no_disc.head(10).iterrows():
    print(f"Row {idx} ASIN {r['asin']} | Price: {r['final_price']} | Buybox: {r['buybox_prices']}")
