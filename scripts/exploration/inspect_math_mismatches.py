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

# Check rows where both init and fin exist, init > fin, and discount has a %
math_mismatches = []
for idx, r in df.iterrows():
    ip = r['init_num']
    fp = r['fin_num']
    d_str = r['discount']
    if ip and fp and ip > fp and d_str:
        m = re.search(r'(\d+(?:\.\d+)?)\s*%', d_str)
        reported_pct = None
        if m:
            reported_pct = float(m.group(1))
        elif re.fullmatch(r'\d+', d_str):
            reported_pct = float(d_str)
        
        if reported_pct is not None:
            calc_pct = (ip - fp) / ip * 100
            diff = abs(calc_pct - reported_pct)
            if diff > 1.0:
                math_mismatches.append({
                    'idx': idx,
                    'asin': r['asin'],
                    'init': ip,
                    'fin': fp,
                    'disc_raw': d_str,
                    'reported_pct': reported_pct,
                    'calc_pct': round(calc_pct, 2),
                    'diff': round(diff, 2)
                })

df_mismatch = pd.DataFrame(math_mismatches)
print(f"Total math mismatches (>1% divergence): {len(df_mismatch)}")
print(df_mismatch.head(15))
