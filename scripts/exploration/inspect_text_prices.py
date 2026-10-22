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

same = df[(df['init_num'] == df['fin_num']) & (~df['discount'].isin(['', 'null']))]

print(f"Checking 87 rows for price mentions in description/features:")
found_mentions = 0
for idx, r in same.iterrows():
    combined_text = r['description'] + " " + r['features'] + " " + r['top_review']
    prices_in_text = re.findall(r'\$\d+(?:\.\d{2})?', combined_text)
    if prices_in_text:
        found_mentions += 1
        if found_mentions <= 5:
            print(f"Row {idx} ASIN {r['asin']} | Price: {r['final_price']} | Disc: {r['discount']} | Text prices: {prices_in_text[:3]}")
print(f"Total rows with price mentions in text: {found_mentions}")
