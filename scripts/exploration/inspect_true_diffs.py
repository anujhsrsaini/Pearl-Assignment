import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import json
import re

df = pd.read_csv('amazon-products.csv', dtype=str, keep_default_na=False)

def clean_price(val):
    if val is None or str(val).strip().lower() in ['', 'null']:
        return None
    # Strip quotes, currency symbols, commas, spaces
    c = re.sub(r'[\"\'$,₹\s]', '', str(val))
    try:
        return float(c)
    except:
        return None

diffs = []
for idx, r in df.iterrows():
    bp_str = r['buybox_prices']
    if bp_str and bp_str != 'null':
        try:
            bp = json.loads(bp_str)
            bp_fin = clean_price(bp.get('final_price'))
            bp_init = clean_price(bp.get('initial_price'))
            col_fin = clean_price(r['final_price'])
            col_init = clean_price(r['initial_price'])
            
            f_diff = (bp_fin is not None and col_fin is not None and abs(bp_fin - col_fin) > 0.01)
            i_diff = (bp_init is not None and col_init is not None and abs(bp_init - col_init) > 0.01)
            
            if f_diff or i_diff:
                diffs.append((idx, r['asin'], col_init, bp_init, col_fin, bp_fin, r['discount']))
        except Exception as e:
            print(f"Row {idx} error: {e}")

print(f"Total true discrepancies between column and buybox: {len(diffs)}")
for d in diffs:
    print(d)
