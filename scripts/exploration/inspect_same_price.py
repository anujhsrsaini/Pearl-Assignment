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

df['init_f'] = df['initial_price'].apply(clean_num)
df['fin_f'] = df['final_price'].apply(clean_num)

# Rows where init == fin and discount is not empty
same_price_with_disc = df[(df['init_f'] == df['fin_f']) & (~df['discount'].isin(['', 'null']))]
print(f"Total rows where init == fin and discount != null: {len(same_price_with_disc)}")

print("\nDiscount distribution in these 87 rows:")
print(same_price_with_disc['discount'].value_counts().head(20))

print("\nCheck if variations column has prices for any of these:")
has_var_prices = 0
for idx, row in same_price_with_disc.head(10).iterrows():
    print(f"\nASIN: {row['asin']} | Price: {row['final_price']} | Discount: {row['discount']}")
    # check variations
    var_str = row['variations']
    if var_str and var_str not in ['null', '[]']:
        try:
            v_data = json.loads(var_str)
            print(f"  Variations count: {len(v_data)}")
            # check first variation
            if len(v_data) > 0:
                print(f"  Sample variation: {list(v_data[0].keys())}")
                if 'price' in v_data[0]:
                    print(f"  Sample var price: {v_data[0].get('price')}")
        except Exception as e:
            print(f"  JSON error: {e}")
