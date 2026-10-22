import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import json
import re

df = pd.read_csv('amazon-products.csv', dtype=str, keep_default_na=False)

def clean_price_val(val):
    if val is None or str(val).strip().lower() in ['', 'null']:
        return None
    c = re.sub(r'[\"\'$,₹\s]', '', str(val))
    try:
        return float(c)
    except:
        return None

def parse_discount_raw(d_str):
    if not d_str or str(d_str).strip().lower() in ['', 'null']:
        return None, None
    s = str(d_str).strip()
    
    # 1. Check for % in string
    pct_match = re.search(r'(\d+(?:\.\d+)?)\s*%', s)
    # 2. Check for currency amount
    curr_match = re.search(r'[\$₹]\s*(\d+(?:\.\d+)?)', s)
    # 3. Check for bare integer
    bare_match = re.fullmatch(r'\d+', s)
    
    pct_val = None
    curr_val = None
    
    if pct_match:
        pct_val = float(pct_match.group(1))
    elif bare_match:
        pct_val = float(bare_match.group(0))
        
    if curr_match:
        curr_val = float(curr_match.group(1))
        
    return pct_val, curr_val

fixed_records = []
for idx, r in df.iterrows():
    init_p = clean_price_val(r['initial_price'])
    fin_p = clean_price_val(r['final_price'])
    raw_d = r['discount']
    pct_d, curr_d = parse_discount_raw(raw_d)
    
    # Check buybox for true prices if available
    bp_fin = None
    bp_init = None
    if r['buybox_prices'] and r['buybox_prices'] != 'null':
        try:
            bp = json.loads(r['buybox_prices'])
            bp_fin = clean_price_val(bp.get('final_price'))
            bp_init = clean_price_val(bp.get('initial_price'))
            # Check sns_price base_price (e.g. Row 992)
            if 'sns_price' in bp and isinstance(bp['sns_price'], dict):
                sns_bp = clean_price_val(bp['sns_price'].get('base_price'))
                if sns_bp:
                    bp_fin = bp_fin or sns_bp
        except:
            pass

    # Fix 1: Known truncated INR prices in final_price (Rows 222, 460, 642)
    if bp_fin and fin_p and bp_fin > fin_p * 5:
        fin_p = bp_fin

    # Fix 2: Inverted price (Row 992) where init=11.39, fin=12.03, disc=$0.91, bp_fin=10.48
    if init_p and fin_p and init_p < fin_p:
        if curr_d and abs((init_p - curr_d) - (bp_fin or 0)) < 0.05:
            fin_p = init_p - curr_d
        elif bp_fin:
            fin_p = bp_fin

    # Fix 3: Missing final_price (Rows 10, 591, 802)
    if fin_p is None:
        if init_p is not None:
            if curr_d is not None:
                fin_p = round(init_p - curr_d, 2)
            elif pct_d is not None:
                fin_p = round(init_p * (1 - pct_d / 100), 2)

    # Fix 4: Missing initial_price (186 rows)
    # Sub-case 4A: Discount is present (61 rows)
    if init_p is None and fin_p is not None:
        if curr_d is not None:
            init_p = round(fin_p + curr_d, 2)
        elif pct_d is not None and pct_d < 100:
            init_p = round(fin_p / (1 - pct_d / 100), 2)
        else:
            # Sub-case 4B: No discount present (125 rows) -> product sold at standard retail price
            init_p = fin_p
            pct_d = 0.0
            curr_d = 0.0

    # Fix 5: Identical prices with discount populated (87 rows)
    # Scraper copied final_price into initial_price. True initial price is fin_p / (1 - pct_d/100)
    if init_p is not None and fin_p is not None and abs(init_p - fin_p) < 0.001:
        if pct_d and pct_d > 0:
            init_p = round(fin_p / (1 - pct_d / 100), 2)
        elif curr_d and curr_d > 0:
            init_p = round(fin_p + curr_d, 2)
        else:
            pct_d = 0.0
            curr_d = 0.0

    # Calculate unified discount metrics
    disc_amount = None
    disc_percent = None
    if init_p is not None and fin_p is not None and init_p > 0:
        disc_amount = round(max(0.0, init_p - fin_p), 2)
        disc_percent = round((disc_amount / init_p) * 100, 2)
        
    fixed_records.append({
        'asin': r['asin'],
        'init_fixed': init_p,
        'fin_fixed': fin_p,
        'disc_amount': disc_amount,
        'disc_percent': disc_percent
    })

df_res = pd.DataFrame(fixed_records)
print("=== RECONCILIATION RESULTS ACROSS ALL 1,000 ROWS ===")
print(f"Total rows: {len(df_res)}")
print(f"initial_price is null: {df_res['init_fixed'].isna().sum()}")
print(f"final_price is null:   {df_res['fin_fixed'].isna().sum()}")
print(f"disc_amount is null:   {df_res['disc_amount'].isna().sum()}")
print(f"disc_percent is null:  {df_res['disc_percent'].isna().sum()}")
print(f"Any init < fin:        {(df_res['init_fixed'] < df_res['fin_fixed']).sum()}")
print(f"Rows with 0% discount: {(df_res['disc_percent'] == 0.0).sum()}")
print(f"Rows with >0% discount:{(df_res['disc_percent'] > 0.0).sum()}")

print("\nSample of previously broken rows after fix:")
for sample_idx in [5, 10, 88, 124, 222, 460, 591, 642, 802, 992]:
    r = df_res.iloc[sample_idx]
    orig_init = df.iloc[sample_idx]['initial_price']
    orig_fin = df.iloc[sample_idx]['final_price']
    orig_disc = df.iloc[sample_idx]['discount']
    print(f"Row {sample_idx:3d} | Orig: init={orig_init}, fin={orig_fin}, disc={repr(orig_disc)}")
    print(f"        | Fixed: init={r['init_fixed']:.2f}, fin={r['fin_fixed']:.2f}, disc_amt={r['disc_amount']:.2f}, disc_%={r['disc_percent']:.2f}%")
