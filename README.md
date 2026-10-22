# Amazon Products Dataset: Quality Audit & Data Cleaning Pipeline

This repository contains the raw and cleaned datasets, analytical audit reports, and an automated data cleaning pipeline for the Amazon Products dataset.

---

## 📌 Table of Contents
1. [Project Overview](#-project-overview)
2. [Repository Directory Structure](#-repository-directory-structure)
3. [Dataset Summary (Before vs After)](#-dataset-summary-before-vs-after)
4. [Identified Formatting & Data Quality Issues](#-identified-formatting--data-quality-issues)
5. [Data Cleaning Methodology & Pipeline](#-data-cleaning-methodology--pipeline)
6. [Verification & Quality Assurance Metrics](#-verification--quality-assurance-metrics)
7. [Cleaned Dataset Schema (60 Columns)](#-cleaned-dataset-schema-60-columns)
8. [How to Reproduce & Execute](#-how-to-reproduce--execute)

---

## 📂 Repository Directory Structure

The repository is organized following clean data engineering and analytical standards:

```text
D:\Anuj\Pearl-ASsignment\
├── data/
│   ├── raw/
│   │   └── amazon-products.csv                     # Original raw input dataset (6.06 MB)
│   └── processed/
│       └── amazon-products-cleaned.csv             # Cleaned, standardized dataset (60 cols, 5.69 MB)
│
├── src/
│   ├── clean_amazon_products.py                    # Automated data cleaning pipeline
│   └── analyze_category_performance.py             # Category benchmarking & business analytics
│
├── reports/
│   ├── BUSINESS_INSIGHTS_CATEGORY_PERFORMANCE.md   # Core business analysis on category performance
│   ├── amazon_products_audit_report.md             # Full structural, schema, & quality audit
│   ├── SELLER_MARKETPLACE_CONCENTRATION_REPORT.md  # Seller competition & concentration report
│   ├── SELLER_ANALYSIS.md                          # Detailed merchant unmasking breakdown
│   └── DATA_RANGE_REPORT.md                        # Numerical distributions & bounds
│
├── scripts/
│   └── exploration/                                # Diagnostic scratch scripts & audits
│       ├── audit_pricing_logic.py
│       ├── seller_concentration_analysis.py
│       └── inspect_*.py
│
├── .gitignore                                      # Standard Python ignore rules
└── README.md                                       # Complete project documentation & data dictionary
```

---

## 🔍 Project Overview

The original dataset ([`data/raw/amazon-products.csv`](./data/raw/amazon-products.csv)) contains raw scraped product metadata from Amazon across various domains (US, IN, UK). To assess data integrity, an autonomous **multi-agent team** was deployed:

- **Agent 1: Structure & Syntax Inspector** — Analyzed byte layouts, line breaks, encoding, CSV dialects, and parser limits.
- **Agent 2: Schema & Type Profiler** — Evaluated all 55 columns, value distributions, missingness patterns, and column semantics.
- **Agent 3: Data Quality & Anomaly Auditor** — Detected text encoding artifacts, price/discount inconsistencies, BiDi markers, and seller obfuscation.

Following the diagnostic audit, an automated cleaning pipeline ([`src/clean_amazon_products.py`](./src/clean_amazon_products.py)) was developed to resolve all identified issues, unmask seller identities, expand nested category trees, and export a standardized, analysis-ready dataset ([`data/processed/amazon-products-cleaned.csv`](./data/processed/amazon-products-cleaned.csv)).

---

## 📊 Dataset Summary (Before vs After)

| Metric / Dimension | Raw Dataset (`data/raw/amazon-products.csv`) | Cleaned Dataset (`data/processed/amazon-products-cleaned.csv`) | Improvement / Impact |
| :--- | :--- | :--- | :--- |
| **File Size** | 6,065,057 bytes (~6.07 MB) | 5,688,648 bytes (~5.69 MB) | Cleaned whitespace, stripped CSS |
| **Physical Line Count** | 1,002 lines | **1,001 lines** | Resolved split row (1 header + 1,000 data rows) |
| **Logical Records** | 1,000 products | **1,000 products** | 100% record retention |
| **Total Columns** | 55 columns | **60 columns** | 3 dead columns dropped, 8 structured columns added |
| **Parser Compatibility** | Crashed line-by-line parsers & python `csv.reader` | **100% compliant** with RFC 4180 & standard loaders | No buffer limits or syntax errors |
| **Categories Expansion** | Serialized JSON string `["Clothing...", "Men"...]` | **7 structured columns** (`level_1` to `level_4`, `leaf`, `path`, `depth`) | Direct SQL/BI filtering without JSON parsing |
| **Price Formatting** | 85.2% quoted (`"""57.79"""`), 177 in sci notation | **100% clean decimals** (e.g. `57.79`, `17.95`) | Directly castable to SQL/Pandas numeric |
| **Redacted Sellers** | 801 sellers masked with `█` (`Ama███.co███`) | **0 redacted sellers** (901 unmasked via buybox) | True merchant identities recovered |
| **BiDi Control Marks** | 300+ occurrences (`\u200e`, `\u200f`) across 7 columns | **0** BiDi marks in dataset | Prevents broken joins and regex errors |
| **Date Format** | Mixed text (`February 17, 2022`, `25 November 2023`) | **100% ISO-8601 `YYYY-MM-DD`** (921 valid dates) | Standardized temporal format |
| **HTML/CSS Noise** | 25 rows with `.aplus-v2` CSS & JS code in description | **100% stripped** to natural product description | Clean text for NLP / text search |
| **Domain Hostnames** | 826 rows had `https://` prefix & `/` suffix | **Normalized** to hostnames (`www.amazon.com`) | Clean categorical dimensions |
| **Discount Metric** | 5 fragmented formats (%, ints, INR, multiline) | **Clean `discount_percentage`** float column | Directly usable in analytics |
| **Null Sentinels** | Inconsistent literal string `'null'` vs empty string | **Standard empty string `""`** across all fields | SQL-safe null representation |

---

## 🛠️ Identified Formatting & Data Quality Issues

### 1. Structural & Syntax Issues
- **Embedded Newline Splitting Row 320:** Row 320 contained a literal `\n` in the `discount` field (`"₹330₹330 (30%) \n (₹55.00 less...)"`), creating 1,002 physical lines and corrupting line-by-line parsers into 27- and 29-column fragments.
- **Python Buffer Overflow:** Rows 162 and 214 contained variations arrays of 151,120 and 144,045 characters, exceeding Python's default `csv.reader` 128 KiB limit (`131072`).
- **Triple-Quoting Artifacts:** 85.2% of rows in `final_price` and 62.5% in `initial_price` were escaped as `"""57.79"""`, parsing into literal strings with quotation marks `'"57.79"'`.

### 2. Semantic & Data Integrity Issues
- **Scientific Notation in Currency:** 177 initial prices and 139 final prices were stored in scientific exponential strings (e.g. `1.795000000000000e+01`). Row 263 contained a comma (`"3,479.00"`).
- **Redacted Merchant Identities:** 801 rows had seller names obscured by black block characters `█` (`\u2588`, e.g. `Orv███tor███`).
- **Invisible Bi-Directional Unicode Pollution:** Scraped Amazon HTML tables injected Left-to-Right (`\u200e`) and Right-to-Left (`\u200f`) marks into metadata columns.
- **Contaminated Descriptions:** 25 descriptions contained raw `.aplus-v2` CSS stylesheets up to 26 KB, inline JavaScript `(function(f) { ... })`, and unescaped HTML entities (`&amp;`, `&gt;`, `&lt;`).
- **Dead / Ghost Columns:** `product_details` (1,000 literal `"null"` strings), `prices_breakdown` (1,000 literal `"null"` strings), and `country_of_origin` (1,000 empty strings) contained zero valid values across all 1,000 rows.
- **Contradictory Video Flags:** In 72 rows, `video == false` despite `video_count > 0`.
- **Typo in Categorical Badge:** 73 rows contained a double space in `"Amazon's  Choice"`.
- **Department Casing Inconsistency:** Fragmented into `womens` vs `Womens` and `mens` vs `Mens`.

---

## 🧹 Data Cleaning Methodology & Pipeline

The remediation logic is encapsulated in [`src/clean_amazon_products.py`](./src/clean_amazon_products.py):

```
Raw CSV: data/raw/amazon-products.csv (55 cols, 1,002 lines)
  │
  ├── 1. Drop 100% Dead Columns (product_details, prices_breakdown, country_of_origin)
  │
  ├── 2. Standardize Null Sentinels (literal 'null' strings -> empty string "")
  │
  ├── 3. Unmask Redacted Sellers (restore 801 '█' masked names from buybox_seller)
  │
  ├── 4. Sanitize Prices (strip quotes, currency symbols, commas; convert scientific notation)
  │
  ├── 5. Normalize Discounts (strip embedded \n; calculate clean discount_percentage)
  │
  ├── 6. Standardize Dates (parse textual date strings -> ISO-8601 YYYY-MM-DD)
  │
  ├── 7. Clean Descriptions (strip .aplus CSS stylesheets, JS code, HTML tags, unescape entities)
  │
  ├── 8. Global Unicode Hygiene (strip \u200e, \u200f, \u200b, \u00a0, C1 controls across all columns)
  │
  ├── 9. Normalize Hostnames & Enums (clean domain, fix badge typo, unify department casing)
  │
  ├── 10. Align Video Flags (video = true when video_count > 0)
  │
  └── 11. Expand Categories (extract path, level_1, level_2, level_3, level_4, leaf, depth)
  │
Cleaned CSV: data/processed/amazon-products-cleaned.csv (60 cols, 1,001 lines)
```

---

## ✅ Verification & Quality Assurance Metrics

Automated test validation on [`data/processed/amazon-products-cleaned.csv`](./data/processed/amazon-products-cleaned.csv) confirmed:

```text
✓ Physical lines: 1001 (1 header + 1000 data rows)
✓ RFC 4180 safe csv.reader: 1001 rows, 60 columns cleanly parsed
✓ Pandas read_csv shape: (1000, 60)
✓ Valid numeric initial_price: 814 / 814 non-empty (186 nulls)
✓ Valid numeric final_price: 997 / 997 non-empty (3 nulls)
✓ Redacted seller_name count: 0 (was 801)
✓ Total BiDi markers in entire dataset: 0 (was 300+)
✓ Valid ISO-8601 dates: 921 / 921 non-empty (0 invalid)
✓ Clean domain hostnames: 100% (www.amazon.com: 967, www.amazon.in: 31, www.amazon.co.uk: 2)
✓ Fixed badge typo: "Amazon's Choice" (73 rows)
✓ Valid numeric discount_percentage: 861 populated (mean: 19.15%, range: 0.0% - 92.6%)
✓ Categories expanded: 100% populated category_level_1, category_level_2, category_leaf, category_path
✓ Video flag contradictions: 0
✓ Total literal 'null' strings: 0
```

---

## 📋 Cleaned Dataset Schema (60 Columns)

| # | Column Name | Data Type | Missing Count (%) | Description |
| :-: | :--- | :--- | :-: | :--- |
| 1 | `timestamp` | `TIMESTAMP` | 0 (0.0%) | Scrape timestamp (ISO-8601) |
| 2 | `title` | `VARCHAR` | 0 (0.0%) | Full product title |
| 3 | `seller_name` | `VARCHAR` | 74 (7.4%) | Unmasked seller / merchant name |
| 4 | `brand` | `VARCHAR` | 1 (0.1%) | Manufacturer brand name |
| 5 | `description` | `TEXT` | 2 (0.2%) | Cleaned product description (CSS/HTML stripped) |
| 6 | `initial_price` | `DECIMAL(10,2)` | 186 (18.6%) | List / original price in product currency |
| 7 | `final_price` | `DECIMAL(10,2)` | 3 (0.3%) | Actual selling price in product currency |
| 8 | `currency` | `CHAR(3)` | 0 (0.0%) | Currency code (`USD`, `INR`, `GBP`) |
| 9 | `availability` | `VARCHAR` | 6 (0.6%) | Stock status (`In Stock`, etc.) |
| 10 | `reviews_count` | `INTEGER` | 0 (0.0%) | Number of customer reviews |
| 11 | `categories` | `JSON ARRAY` | 0 (0.0%) | Original raw JSON category hierarchy array |
| 12 | `category_path` | `VARCHAR` | 0 (0.0%) | Expanded category breadcrumb path (`> ` delimited) |
| 13 | `category_level_1` | `VARCHAR` | 0 (0.0%) | Top-level root category (e.g. `Clothing, Shoes & Jewelry`) |
| 14 | `category_level_2` | `VARCHAR` | 0 (0.0%) | Secondary subcategory (e.g. `Men`, `Kitchen & Dining`) |
| 15 | `category_level_3` | `VARCHAR` | 4 (0.4%) | Tertiary subcategory (e.g. `Shoes`, `Bedding`) |
| 16 | `category_level_4` | `VARCHAR` | 82 (8.2%) | Level 4 subcategory |
| 17 | `category_leaf` | `VARCHAR` | 0 (0.0%) | Terminal / deepest category name (e.g. `Road Running`) |
| 18 | `category_depth` | `INTEGER` | 0 (0.0%) | Total number of hierarchy levels (range: 2 to 9) |
| 19 | `asin` | `CHAR(10)` | 0 (0.0%) | Amazon Standard Identification Number (Primary Key) |
| 20 | `buybox_seller` | `VARCHAR` | 74 (7.4%) | Winning buy box merchant |
| 21 | `number_of_sellers` | `INTEGER` | 16 (1.6%) | Count of competing marketplace sellers |
| 22 | `root_bs_rank` | `INTEGER` | 1 (0.1%) | Best seller rank in top-level category |
| 23 | `answered_questions`| `INTEGER` | 31 (3.1%) | Count of answered customer Q&A |
| 24 | `domain` | `VARCHAR` | 0 (0.0%) | Standardized Amazon hostname |
| 25 | `images_count` | `INTEGER` | 0 (0.0%) | Number of product images available |
| 26 | `url` | `VARCHAR` | 0 (0.0%) | Canonical product URL (HTTPS) |
| 27 | `video_count` | `INTEGER` | 0 (0.0%) | Number of product videos |
| 28 | `image_url` | `VARCHAR` | 5 (0.5%) | Primary product image CDN URL |
| 29 | `item_weight` | `VARCHAR` | 247 (24.7%) | Product physical weight with units |
| 30 | `rating` | `DECIMAL(2,1)` | 0 (0.0%) | Average customer rating (1.0 to 5.0) |
| 31 | `product_dimensions`| `VARCHAR` | 67 (6.7%) | Physical dimensions |
| 32 | `seller_id` | `VARCHAR` | 0 (0.0%) | Amazon merchant token ID |
| 33 | `date_first_available`| `DATE` | 79 (7.9%) | First listed date (`YYYY-MM-DD`) |
| 34 | `discount` | `VARCHAR` | 179 (17.9%) | Raw cleaned discount text string |
| 35 | `discount_percentage`| `DECIMAL(5,2)` | 139 (13.9%) | Calculated / standardized discount percentage (0–100) |
| 36 | `model_number` | `VARCHAR` | 108 (10.8%) | Manufacturer part / model number |
| 37 | `manufacturer` | `VARCHAR` | 30 (3.0%) | Manufacturing company |
| 38 | `department` | `VARCHAR` | 338 (33.8%) | Target department (`Womens`, `Mens`, etc.) |
| 39 | `plus_content` | `BOOLEAN` | 0 (0.0%) | Whether A+ enhanced content is present (`true`/`false`) |
| 40 | `upc` | `VARCHAR` | 901 (90.1%) | Universal Product Code(s) |
| 41 | `video` | `BOOLEAN` | 0 (0.0%) | Video presence indicator (`true`/`false`) |
| 42 | `top_review` | `TEXT` | 8 (0.8%) | Top highlighted customer review excerpt |
| 43 | `variations` | `JSON ARRAY` | 319 (31.9%) | JSON array of product variation SKUs |
| 44 | `delivery` | `JSON ARRAY` | 54 (5.4%) | JSON array of delivery promises |
| 45 | `features` | `JSON ARRAY` | 201 (20.1%) | JSON array of key feature bullets |
| 46 | `format` | `JSON ARRAY` | 998 (99.8%) | Audio / media format specifications |
| 47 | `buybox_prices` | `JSON OBJECT` | 182 (18.2%) | JSON object of buy box and SnS prices |
| 48 | `parent_asin` | `CHAR(10)` | 617 (61.7%) | Parent container ASIN for SKU variations |
| 49 | `input_asin` | `CHAR(10)` | 627 (62.7%) | Initial crawl seed ASIN |
| 50 | `ingredients` | `TEXT` | 954 (95.4%) | Ingredient breakdown for consumables |
| 51 | `origin_url` | `VARCHAR` | 759 (75.9%) | Source browse category URL |
| 52 | `bought_past_month` | `INTEGER` | 796 (79.6%) | Estimated purchases in the past month |
| 53 | `is_available` | `BOOLEAN` | 783 (78.3%) | In-stock indicator flag |
| 54 | `root_bs_category` | `VARCHAR` | 894 (89.4%) | Top-level Best Sellers category name |
| 55 | `bs_category` | `VARCHAR` | 894 (89.4%) | Specific leaf category name |
| 56 | `bs_rank` | `INTEGER` | 894 (89.4%) | Best Sellers rank in leaf category |
| 57 | `badge` | `VARCHAR` | 924 (92.4%) | Product marketing badge (`Amazon's Choice`, etc.) |
| 58 | `subcategory_rank` | `JSON ARRAY` | 895 (89.5%) | Nested subcategory ranks JSON array |
| 59 | `amazon_choice` | `BOOLEAN` | 894 (89.4%) | Amazon's Choice boolean indicator |
| 60 | `images` | `JSON ARRAY` | 948 (94.8%) | JSON array of high-resolution image URLs |

---

## 🚀 How to Reproduce & Execute

### 1. Run Data Cleaning Pipeline
```bash
python src/clean_amazon_products.py
```
Reads [`data/raw/amazon-products.csv`](./data/raw/amazon-products.csv) and outputs [`data/processed/amazon-products-cleaned.csv`](./data/processed/amazon-products-cleaned.csv).

### 2. Run Category Performance Analytics
```bash
python src/analyze_category_performance.py
```
Computes and displays category benchmark metrics across catalog presence, ratings, and review volumes.
