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

col_vs_buybox_diffs = []
for idx, r in df.iterrows():
    bp_str = r['buybox_prices']
    if bp_str and bp_str != 'null':
        try:
            bp = json.loads(bp_str)
            bp_fin = clean_num(bp.get('final_price'))
            bp_init = clean_num(bp.get('initial_price'))
            
            f_diff = False
            i_diff = False
            if bp_fin is not None and r['fin_num'] is not None and abs(bp_fin - r['fin_num']) > 0.01:
                f_diff = True
            if bp_init is not None and r['init_num'] is not None and abs(bp_init - r['init_num']) > 0.01:
                i_diff = True
            
            if f_diff or i_diff:
                col_vs_buybox_diffs.append({
                    'idx': idx,
                    'asin': r['asin'],
                    'col_init': r['init_num'],
                    'bp_init': bp_init,
                    'col_fin': r['fin_num'],
                    'bp_fin': bp_fin,
                    'disc': r['discount']
                })
        except Exception as e:
            pass

diff_df = pd.DataFrame(col_vs_buybox_diffs)
print(f"Total rows where column price != buybox_prices: {len(diff_df)}")
print(diff_df)
