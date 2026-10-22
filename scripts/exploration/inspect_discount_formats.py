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

df['init_f'] = df['initial_price'].apply(clean_num)
df['fin_f'] = df['final_price'].apply(clean_num)

g_diff = df[df['init_f'] > df['fin_f']]
print("Discount samples when initial_price > final_price (669 rows):")
print(g_diff['discount'].value_counts().head(25))

print("\nAre there negative discounts in init > fin?")
neg_in_diff = g_diff[g_diff['discount'].str.startswith('-')]
print(f"Count of negative discounts in init > fin: {len(neg_in_diff)}")
if len(neg_in_diff) > 0:
    print(neg_in_diff[['asin', 'initial_price', 'final_price', 'discount']].head())
