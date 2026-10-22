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

print(f"Number of rows where init == fin and discount is not null: {len(same)}")
print("\nCheck buybox_prices in these 87 rows:")
buybox_has_diff = 0
for idx, r in same.iterrows():
    bp = r['buybox_prices']
    if bp and bp != 'null':
        try:
            d = json.loads(bp)
            # check keys
            init_bp = d.get('initial_price')
            fin_bp = d.get('final_price')
            disc_bp = d.get('discount')
            if init_bp != fin_bp and init_bp is not None:
                buybox_has_diff += 1
                print(f"Row {idx} ASIN {r['asin']}: init_bp={init_bp}, fin_bp={fin_bp}, disc_bp={disc_bp}")
        except:
            pass

print(f"buybox_prices has different prices in {buybox_has_diff} rows.")
