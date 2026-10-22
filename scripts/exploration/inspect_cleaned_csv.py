import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

df_clean = pd.read_csv('amazon-products-cleaned.csv', dtype=str, keep_default_na=False)
print("=== AMAZON-PRODUCTS-CLEANED.CSV STATUS ===")
print("Shape:", df_clean.shape)

init_null = (df_clean['initial_price'] == '')
fin_null = (df_clean['final_price'] == '')
disc_null = (df_clean['discount'] == '')
disc_pct_null = (df_clean['discount_percentage'] == '')

print(f"initial_price empty: {init_null.sum()}")
print(f"final_price empty: {fin_null.sum()}")
print(f"discount empty: {disc_null.sum()}")
print(f"discount_percentage empty: {disc_pct_null.sum()}")

print("\nValue counts of discount_percentage (top 15):")
print(df_clean['discount_percentage'].value_counts().head(15))

print("\nHow many discount_percentage are '0.00'?")
print((df_clean['discount_percentage'] == '0.00').sum())

print("\nLet's check the rows where discount_percentage is '0.00':")
sample_zero = df_clean[df_clean['discount_percentage'] == '0.00'][['asin', 'initial_price', 'final_price', 'discount', 'discount_percentage']].head(10)
print(sample_zero)
