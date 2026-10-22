import os
import csv
import re
import html
import json
import unicodedata
from datetime import datetime
import numpy as np
import pandas as pd

csv.field_size_limit(2147483647)

# Flexible path resolution relative to repo root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

# Resolve input file path
candidates_input = [
    os.path.join(REPO_ROOT, "data", "raw", "amazon-products.csv"),
    os.path.join(REPO_ROOT, "amazon-products.csv"),
    os.path.join(os.getcwd(), "data", "raw", "amazon-products.csv"),
    os.path.join(os.getcwd(), "amazon-products.csv")
]
INPUT_FILE = next((p for p in candidates_input if os.path.exists(p)), candidates_input[0])

# Output path defaults to data/processed/amazon-products-cleaned.csv
OUTPUT_DIR = os.path.join(REPO_ROOT, "data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "amazon-products-cleaned.csv")

def clean_css_and_text(s):
    if not s or str(s).strip().lower() == 'null':
        return ''
    s = str(s).replace('\x96', '–').replace('\x85', '…')
    s = html.unescape(s)
    s = re.sub(r'<style[^>]*>.*?</style>', '', s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r'<script[^>]*>.*?</script>', '', s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.DOTALL)
    prev = None
    while prev != s and '{' in s and '}' in s:
        prev = s
        s = re.sub(r'[^{};>]*\{[^{}]*\}', '', s)
    s = re.sub(r'\.aplus-[^\s]+', '', s)
    s = re.sub(r'\.apm-[^\s]+', '', s)
    s = re.sub(r'@media[^\)]+\)', '', s)
    s = re.sub(r'html\[[^\]]+\]', '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\(function\([^\)]*\)\s*\{.*?\}\);?', '', s, flags=re.DOTALL)
    s = re.sub(r'[\u200e\u200f\u200b\u200c\u200d]', '', s)
    s = s.replace('\u00a0', ' ')
    s = unicodedata.normalize('NFKD', s)
    return re.sub(r'\s+', ' ', s).strip()

def clean_price(val):
    if not val or str(val).strip().lower() == 'null':
        return ''
    cleaned = re.sub(r'[\"\'$,₹\s]', '', str(val))
    try:
        f = float(cleaned)
        return f"{f:.2f}"
    except ValueError:
        return ''

def parse_date(d_str):
    if not d_str or str(d_str).strip().lower() == 'null':
        return ''
    cleaned = re.sub(r'[\u200e\u200f]', '', str(d_str)).strip()
    if not cleaned:
        return ''
    for fmt in ('%B %d, %Y', '%d %B %Y', '%b %d, %Y', '%d %b %Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(cleaned, fmt).strftime('%Y-%m-%d')
        except ValueError:
            pass
    try:
        from dateutil import parser
        return parser.parse(cleaned).strftime('%Y-%m-%d')
    except:
        return cleaned

def run_cleaning():
    print(f"Reading raw data from: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False, engine='c')
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns.")

    # 1. Drop 100% dead columns
    dead_cols = ['product_details', 'prices_breakdown', 'country_of_origin']
    df = df.drop(columns=[c for c in dead_cols if c in df.columns])
    print(f"Dropped dead columns: {dead_cols}")

    # 2. Harmonize 'null' string sentinels across all columns to empty string
    for col in df.columns:
        df[col] = df[col].apply(lambda x: '' if str(x).strip().lower() == 'null' else str(x))

    # 3. Clean seller_name: unmask redacted names using buybox_seller
    mask_redacted = df['seller_name'].str.contains('█', na=False) | (df['seller_name'] == '')
    can_restore = mask_redacted & (df['buybox_seller'] != '')
    df.loc[can_restore, 'seller_name'] = df.loc[can_restore, 'buybox_seller']
    print(f"Restored {can_restore.sum()} seller names using buybox_seller.")

    # 4 & 5. Advanced Pricing & Discount Mathematical Reconciliation
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
        pct_match = re.search(r'(\d+(?:\.\d+)?)\s*%', s)
        curr_match = re.search(r'[\$₹]\s*(\d+(?:\.\d+)?)', s)
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

    init_cleaned = []
    fin_cleaned = []
    disc_amt_cleaned = []
    disc_pct_cleaned = []
    disc_text_cleaned = []

    for idx, row in df.iterrows():
        ip = clean_price_val(row['initial_price'])
        fp = clean_price_val(row['final_price'])
        raw_d = row['discount']
        pct_d, curr_d = parse_discount_raw(raw_d)
        
        # Check buybox_prices for ground-truth figures
        bp_fin = None
        bp_init = None
        if row.get('buybox_prices') and row['buybox_prices'] != 'null':
            try:
                bp = json.loads(row['buybox_prices'])
                bp_fin = clean_price_val(bp.get('final_price'))
                bp_init = clean_price_val(bp.get('initial_price'))
                if 'sns_price' in bp and isinstance(bp['sns_price'], dict):
                    sns_bp = clean_price_val(bp['sns_price'].get('base_price'))
                    if sns_bp:
                        bp_fin = bp_fin or sns_bp
            except:
                pass
                
        # Fix 1: Truncated INR prices in final_price column (Rows 222, 460, 642)
        if bp_fin and fp and bp_fin > fp * 5:
            fp = bp_fin

        # Fix 2: Inverted price (Row 992)
        if ip and fp and ip < fp:
            if curr_d and abs((ip - curr_d) - (bp_fin or 0)) < 0.05:
                fp = round(ip - curr_d, 2)
            elif bp_fin:
                fp = bp_fin

        # Fix 3: Missing final_price (Rows 10, 591, 802)
        if fp is None and ip is not None:
            if curr_d is not None:
                fp = round(ip - curr_d, 2)
            elif pct_d is not None:
                fp = round(ip * (1 - pct_d / 100), 2)

        # Fix 4: Missing initial_price (186 rows)
        if ip is None and fp is not None:
            if curr_d is not None:
                ip = round(fp + curr_d, 2)
            elif pct_d is not None and pct_d < 100:
                ip = round(fp / (1 - pct_d / 100), 2)
            else:
                ip = fp
                pct_d = 0.0
                curr_d = 0.0

        # Fix 5: Disentangle identical prices with active discount (87 rows)
        if ip is not None and fp is not None and abs(ip - fp) < 0.001:
            if pct_d and pct_d > 0:
                ip = round(fp / (1 - pct_d / 100), 2)
            elif curr_d and curr_d > 0:
                ip = round(fp + curr_d, 2)
            else:
                pct_d = 0.0
                curr_d = 0.0

        # Calculate unified, mathematically guaranteed metrics
        if ip is not None and fp is not None and ip > 0:
            d_amt = round(max(0.0, ip - fp), 2)
            d_pct = round((d_amt / ip) * 100, 2)
        else:
            d_amt = 0.0
            d_pct = 0.0

        init_cleaned.append(f"{ip:.2f}" if ip is not None else "")
        fin_cleaned.append(f"{fp:.2f}" if fp is not None else "")
        disc_amt_cleaned.append(f"{d_amt:.2f}")
        disc_pct_cleaned.append(f"{d_pct:.2f}")
        
        # Clean display text for discount
        if raw_d:
            s = raw_d.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
            disc_text_cleaned.append(re.sub(r'\s+', ' ', s).strip())
        else:
            disc_text_cleaned.append('')

    df['initial_price'] = init_cleaned
    df['final_price'] = fin_cleaned
    df['discount'] = disc_text_cleaned
    df['discount_amount'] = disc_amt_cleaned
    df['discount_percentage'] = disc_pct_cleaned

    # 6. Standardize date_first_available to YYYY-MM-DD
    df['date_first_available'] = df['date_first_available'].apply(parse_date)

    # 7. Normalize domain
    def clean_domain(val):
        if not val:
            return ''
        d = re.sub(r'^https?://', '', str(val))
        return d.rstrip('/')
    df['domain'] = df['domain'].apply(clean_domain)

    # 8. Fix badge double-space typo
    df['badge'] = df['badge'].replace({"Amazon's  Choice": "Amazon's Choice"})

    # 9. Clean description
    df['description'] = df['description'].apply(clean_css_and_text)

    # 10. Clean availability
    df['availability'] = df['availability'].apply(lambda a: 'In Stock' if a.strip() in ['In Stock', 'In Stock.'] else a.strip())

    # 11. Fix video contradiction
    video_has_count = df['video_count'].apply(lambda c: int(c) if c.isdigit() else 0) > 0
    df.loc[video_has_count, 'video'] = 'true'

    # 12. Strip invisible BiDi and control characters across EVERY column
    def strip_invisible_all(val):
        if not val or not isinstance(val, str):
            return val
        s = re.sub(r'[\u200e\u200f\u200b\u200c\u200d]', '', val)
        s = s.replace('\u00a0', ' ')
        s = s.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
        s = unicodedata.normalize('NFKD', s)
        return s.strip()

    for col in df.columns:
        if col != 'description':
            df[col] = df[col].apply(strip_invisible_all)

    # 13. Clean department casing
    dept_map = {
        'womens': 'Womens',
        'mens': 'Mens',
        'unisex-adult': 'Unisex Adult',
        'girls': 'Girls',
        'boys': 'Boys'
    }
    df['department'] = df['department'].apply(lambda d: dept_map.get(d, d))

    # 14. EXPAND CATEGORIES LIST INTO STRUCTURED HIERARCHY COLUMNS
    def parse_cat_list(val):
        try:
            arr = json.loads(val)
            if isinstance(arr, list):
                return arr
        except:
            pass
        return []

    cats_parsed = df['categories'].apply(parse_cat_list)
    df['category_path'] = cats_parsed.apply(lambda arr: " > ".join(arr) if arr else "")
    df['category_level_1'] = cats_parsed.apply(lambda arr: arr[0] if len(arr) > 0 else "")
    df['category_level_2'] = cats_parsed.apply(lambda arr: arr[1] if len(arr) > 1 else "")
    df['category_level_3'] = cats_parsed.apply(lambda arr: arr[2] if len(arr) > 2 else "")
    df['category_level_4'] = cats_parsed.apply(lambda arr: arr[3] if len(arr) > 3 else "")
    df['category_leaf'] = cats_parsed.apply(lambda arr: arr[-1] if len(arr) > 0 else "")
    df['category_depth'] = cats_parsed.apply(len).astype(str)

    # Reorder columns
    cols = list(df.columns)
    for c in ['category_path', 'category_level_1', 'category_level_2', 'category_level_3', 'category_level_4', 'category_leaf', 'category_depth']:
        cols.remove(c)
    cat_idx = cols.index('categories')
    for i, c in enumerate(['category_path', 'category_level_1', 'category_level_2', 'category_level_3', 'category_level_4', 'category_leaf', 'category_depth']):
        cols.insert(cat_idx + 1 + i, c)

    for c in ['discount_amount', 'discount_percentage']:
        if c in cols:
            cols.remove(c)
    disc_idx = cols.index('discount')
    cols.insert(disc_idx + 1, 'discount_amount')
    cols.insert(disc_idx + 2, 'discount_percentage')

    df = df[cols]

    print(f"\nFinal cleaned dataset shape: {df.shape}")
    print(f"Exporting to: {OUTPUT_FILE}...")
    df.to_csv(OUTPUT_FILE, index=False, quoting=csv.QUOTE_MINIMAL, encoding='utf-8', lineterminator='\n')
    print("Export complete!")

if __name__ == '__main__':
    run_cleaning()
