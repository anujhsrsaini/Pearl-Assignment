import pandas as pd
import json

df = pd.read_csv('amazon-products.csv', dtype=str, keep_default_na=False)
r = df.iloc[222]
print("Row 222:")
print("final_price:", repr(r['final_price']))
print("buybox_prices:", repr(r['buybox_prices']))
bp = json.loads(r['buybox_prices'])
print("bp final_price:", repr(bp.get('final_price')))
