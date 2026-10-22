import sys
import codecs
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

print("=== 1. NULL / MISSING ANALYSIS ===")
print(f"Total records: {len(df)}")
print(f"initial_price == '' or 'null': {(df['initial_price'].isin(['', 'null'])).sum()}")
print(f"final_price == '' or 'null':   {(df['final_price'].isin(['', 'null'])).sum()}")
print(f"discount == '' or 'null':      {(df['discount'].isin(['', 'null'])).sum()}")

print("\nCross-tabulation of nullity:")
print(pd.crosstab(
    df['init_num'].isna().rename('initial_is_null'),
    df['fin_num'].isna().rename('final_is_null'),
    margins=True
))

print("\nCross-tab of initial_price nullity vs discount nullity:")
print(pd.crosstab(
    df['init_num'].isna().rename('initial_is_null'),
    df['discount'].isin(['', 'null']).rename('discount_is_null'),
    margins=True
))

print("\n=== 2. DISCOUNT TEXT FORMAT ANALYSIS ===")
disc_series = df['discount'].replace('', 'NULL').replace('null', 'NULL')

def categorize_discount(d):
    if d == 'NULL':
        return 'NULL / Empty'
    if re.fullmatch(r'-\d+%', d):
        return 'Negative Percentage (e.g. -20%)'
    if re.fullmatch(r'\d+%', d):
        return 'Positive Percentage (e.g. 20%)'
    if re.fullmatch(r'\d+', d):
        return 'Bare Integer (e.g. 15, 37)'
    if 'less than buying' in d:
        return 'Bundle / Comparative Text (e.g. less than buying separately)'
    if ('$' in d or '₹' in d) and '%' in d:
        return 'Currency + Percentage (e.g. $8.88 (19%))'
    if '$' in d or '₹' in d:
        return 'Currency only (e.g. $7.00, $0.91)'
    return f'Other: {repr(d[:20])}'

df['disc_category'] = disc_series.apply(categorize_discount)
print(df['disc_category'].value_counts())
