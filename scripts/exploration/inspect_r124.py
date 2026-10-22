import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

df = pd.read_csv('amazon-products.csv', dtype=str, keep_default_na=False)

r124 = df.iloc[124]
print("Row 124:")
print("Title:", r124['title'])
print("Features:", r124['features'])
print("Top review:", r124['top_review'])
