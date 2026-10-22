import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

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

diff_sample = df[df['init_num'] > df['fin_num']][['asin', 'title', 'initial_price', 'final_price', 'discount']].head(10)
for idx, r in diff_sample.iterrows():
    ip = r['initial_num'] = clean_num(r['initial_price'])
    fp = r['fin_num'] = clean_num(r['final_price'])
    calc_pct = round((ip - fp) / ip * 100)
    print(f"ASIN: {r['asin']} | Init: {ip} | Fin: {fp} | Disc: {r['discount']} | Calc%: {calc_pct}%")
