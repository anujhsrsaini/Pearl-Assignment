# Amazon Products Dataset: Quality Audit, AI-First Cleaning & Strategic Analysis

[![Dataset: Scraped Amazon](https://img.shields.io/badge/Dataset-Amazon_Products_(1%2C000_records)-orange.svg)](./data/raw/amazon-products.csv)
[![Cleaned Records: 100%](https://img.shields.io/badge/Cleaned_Data-60_Columns_Standardized-green.svg)](./data/processed/amazon-products-cleaned.csv)
[![AI Assistant: Antigravity CLI](https://img.shields.io/badge/AI_Pair_Programmer-Antigravity_CLI_(Gemini_3.8_Flash)-blue.svg)](./antigravity_conversations/)
[![Assessment Writeup](https://img.shields.io/badge/Executive_Summary-PDF_Available-red.svg)](./reports/ASSESSMENT_EXECUTIVE_SUMMARY.pdf)

> **Submission Brief:** This repository contains the live evaluation submission for the AI-First Analytics Engineer assessment. It demonstrates an AI-first workflow on unfamiliar, scraped eCommerce data (~1,000 Amazon product listings from Luminati/BrightData), orchestrating autonomous specialized agents to audit, clean, verify, and extract verified business insights under live time constraints.

---

## 🎯 Reviewer Quick Links (The Assessment Deliverables)

| Deliverable | Description | Direct Link |
| :--- | :--- | :---: |
| 📄 **Executive Summary Memo** | Non-technical briefing for the Category Manager (answers all 4 prompt questions) | [**ASSESSMENT_EXECUTIVE_SUMMARY.pdf**](./reports/ASSESSMENT_EXECUTIVE_SUMMARY.pdf) &nbsp;([Markdown](./reports/ASSESSMENT_EXECUTIVE_SUMMARY.md)) |
| 💬 **AI Session Transcripts** | Complete, unedited conversation logs across all 4 parallel terminal sessions & subagents | [**antigravity_conversations/**](./antigravity_conversations/) |
| 🧹 **Cleaned Production Data** | Sanitized, 60-column dataset with expanded category trees & unmasked sellers | [**amazon-products-cleaned.csv**](./data/processed/amazon-products-cleaned.csv) |
| ⚙️ **Automated Pipeline Code** | Reproducible, standalone Python cleaning & expansion pipeline | [**clean_amazon_products.py**](./src/clean_amazon_products.py) |
| 📊 **Category Strategy Report** | Deep-dive category benchmarking based on 100% verified data | [**BUSINESS_INSIGHTS_CATEGORY_PERFORMANCE.md**](./reports/BUSINESS_INSIGHTS_CATEGORY_PERFORMANCE.md) |
| 🔍 **Full 55-Col Audit Report** | Complete pre-cleaning diagnostic audit report | [**amazon_products_audit_report.md**](./reports/amazon_products_audit_report.md) |

---

## ⚡ Executive Answers to the Assessment Brief

### 1. Get Oriented: What is this data, and would you trust it?
* **What it is:** A cross-sectional snapshot of 1,000 scraped Amazon product listings containing 55 raw attributes (identifiers, pricing, taxonomy, ratings, seller metadata, and serialized JSON payloads).
* **Would I trust it raw? No.** Naive ingestion fails immediately:
  - **Silent Row Split:** Row 320 contains a literal newline (`\n`) inside the `discount` field, breaking line-by-line parsers into 27- and 29-column fragments.
  - **Buffer Limit Crash:** Variation arrays in Rows 162 and 214 exceed 144–151 KB, crashing standard Python CSV readers (`_csv.Error: field larger than field limit`).
  - **Price Corruption:** 85.2% of `final_price` values are escaped as `"""57.79"""` (string with literal quotes), and 177 prices are in scientific notation (`1.795e+01`).
  - **Dead Columns & Redactions:** 3 columns are 100% dead (`product_details`, `prices_breakdown`, `country_of_origin`), and 801 seller names are masked with black block glyphs (`█`).
* **What was fixed first:** Executed an automated multi-agent triage: sanitized prices to decimal floats, resolved the split line, unmasked seller identities via buybox data, stripped invisible BiDi marks (`\u200e`/`\u200f`), and expanded category trees into 7 queryable columns.

---

### 2. Business Question: "Which product category should we prioritise, and why?"
**Recommendation to Category Manager:** Prioritise **Home & Kitchen** as the core volume growth driver, paired with **Tools & Home Improvement** for rapid, low-cost market entry.

#### Category Performance Benchmark (100% Verified Data)
| Category | Catalog Share | Total Reviews | Median Reviews | Mean Rating | Strategic Assessment |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Home & Kitchen** | **15.0%** (150) | 417,487 (12.9%) | 498.5 | **4.47 / 5.0** | **Primary Target:** High customer delight (4.47), massive addressable catalog, surmountable social proof barrier (~500 reviews). |
| **Tools & Home Improvement** | **11.2%** (112) | 104,117 (3.2%) | 221.5 | **4.38 / 5.0** | **Low-Hanging Fruit:** Lowest review barrier among major categories (221 median). Fast path for new listings to achieve search rank parity. |
| **Clothing, Shoes & Jewelry** | 21.6% (216) | 951,495 (29.3%) | 924.5 | 4.36 / 5.0 | **Saturated Moat:** Largest volume, but entrenched review moat (>920 median) requires massive ad spend to compete. |
| **Pet Supplies** | 2.6% (26) | 409,036 (12.6%) | **2,007.5** | 4.35 / 5.0 | **Extreme Moat:** Phenomenal review density (2,008 median reviews), but entry barriers for unproven brands are severe. |
| **Beauty** | 3.1% (31) | 110,555 (3.4%) | 114.0 | **4.06 / 5.0** | **High Friction:** Lowest rating on Amazon (4.06 vs 4.40 platform avg). Elevated return and customer dissatisfaction risks. |

* **What the data supports:** Relative catalog dominance, social proof barriers (`reviews_count`), and customer satisfaction benchmarks (`rating`).
* **What the data DOES NOT support:** True unit sales volume, gross margins, customer acquisition cost (CAC), conversion rates, or return rates (sales velocity and cost breakdowns are 80%–100% missing).

---

### 3. Data Skepticism: What you must verify before taking action
* **Phantom Discounts (87 Rows):** In 87 listings, `initial_price == final_price` down to the cent, yet non-zero discounts (up to -82%) are listed. Raw discounts are promotional display badges, not financial ground truths.
* **Multi-Currency Poisoning:** The dataset mixes USD (96.7%), INR (3.1%), and GBP (0.2%). Comparing prices without foreign exchange conversion will distort pricing tiers.
* **Unreliable Sales Velocity (`bought_past_month`):** 79.6% missing; remaining values are rounded marketing thresholds (50, 100, 1000). It cannot be used for inventory planning.

---

### 4. Something You Didn't Ask: Observations Beyond the Brief
1. **Competitive Intelligence / Scraper Redaction Leak:** While `seller_name` was intentionally masked with black block glyphs (`█`) in 801 rows for privacy, the scraper inadvertently captured `buybox_seller` completely unmasked. This allowed us to 100% reverse-engineer vendor identities and map Amazon 1P retail vs 3P merchant dominance.
2. **The Question I Wanted to Answer but Couldn't:** *"Does Amazon systematically prioritize its own private-label products (Amazon Essentials) over 3P merchants in the Buy Box when competing on identical price?"* — Cannot be definitively proven because competitor bid logs (`prices_breakdown`) are 100% dead.

---

## 🤖 AI-First Engineering Methodology

Rather than running ad-hoc prompts, this evaluation operated as an **autonomous multi-agent system**:

```text
                                [ User / Candidate ]
                                         │
                   ┌─────────────────────┼─────────────────────┐
                   ▼                     ▼                     ▼
             [ Terminal 1 ]        [ Terminal 2 ]        [ Terminal 3 / 4 ]
           Lead Orchestrator         Data Ranges           Pricing Logic &
           & Cleaning Engine       & Seller Masks        Seller Dominance
                   │
         ┌─────────┼─────────┐
         ▼         ▼         ▼
    [ Subagent 1 ] [ Subagent 2 ] [ Subagent 3 ]
       Syntax        Schema          Quality
      Inspector     Profiler         Auditor
```

1. **Agent Specialization:** Divided responsibilities across parallel agents (physical byte inspection, schema typing, semantic anomaly auditing).
2. **Verification Over Blind Trust:** Every assertion made by the AI models was cross-examined with automated Python verification scripts (`verify_cleaned.py`, `check_prices.py`) before accepting results.
3. **Reproducible Code Generation:** All fixes were baked into production-ready, idempotent scripts rather than manual one-off edits.

---

## 📂 Repository Directory Layout

```text
anujhsrsaini/Pearl-Assignment/
|-- README.md                                       # Executive assessment overview & documentation
|-- .gitignore                                      # Python & OS ignore rules
|
|-- data/
|   |-- raw/
|   |   `-- amazon-products.csv                     # Original raw dataset (55 cols, 6.06 MB)
|   `-- processed/
|       `-- amazon-products-cleaned.csv             # Cleaned, standardized dataset (60 cols, 5.69 MB)
|
|-- src/
|   |-- clean_amazon_products.py                    # Production cleaning & category expansion pipeline
|   |-- analyze_category_performance.py             # Category performance analytics script
|   `-- analyze_seller_concentration.py             # Seller market dominance analytics script
|
|-- reports/
|   |-- ASSESSMENT_EXECUTIVE_SUMMARY.pdf            # Presentation-ready Executive PDF Brief
|   |-- ASSESSMENT_EXECUTIVE_SUMMARY.md             # Markdown version of Executive Summary
|   |-- BUSINESS_INSIGHTS_CATEGORY_PERFORMANCE.md   # Detailed category benchmarking analysis
|   |-- amazon_products_audit_report.md             # Full 55-column diagnostic audit report
|   |-- SELLER_MARKETPLACE_CONCENTRATION_REPORT.md  # Seller competition & concentration report
|   |-- SELLER_ANALYSIS.md                          # Seller name unmasking breakdown
|   `-- DATA_RANGE_REPORT.md                        # Numerical distributions & bounds
|
|-- antigravity_conversations/                      # All Antigravity CLI transcripts & readable logs
|   |-- README.md                                   # Transcript directory index
|   |-- TERMINAL_1_LEAD_ORCHESTRATOR.md             # Terminal 1 lead agent log
|   |-- TERMINAL_1_SUBAGENT_STRUCTURE_INSPECTOR.md  # Terminal 1 subagent 1 log
|   |-- TERMINAL_1_SUBAGENT_SCHEMA_PROFILER.md      # Terminal 1 subagent 2 log
|   |-- TERMINAL_1_SUBAGENT_QUALITY_AUDITOR.md      # Terminal 1 subagent 3 log
|   |-- TERMINAL_2_DATA_RANGE_AND_SELLER_ANALYSIS.md# Terminal 2 session log
|   |-- TERMINAL_3_PRICING_AND_DISCOUNT_DEEP_DIVE.md# Terminal 3 session log
|   |-- TERMINAL_4_SELLER_CONCENTRATION_ORCHESTRATOR.md# Terminal 4 session log
|   |-- TERMINAL_4_SUBAGENT_1.md                    # Terminal 4 subagent 1 log
|   |-- TERMINAL_4_SUBAGENT_2.md                    # Terminal 4 subagent 2 log
|   `-- raw_transcripts/                            # Raw JSONL transcripts for all sessions
|
`-- scripts/exploration/                            # Scratch diagnostic scripts (inspect_*.py, audit_*.py)
```

---

## 📊 Dataset Comparison: Raw vs. Cleaned

| Metric / Dimension | Raw (`data/raw/amazon-products.csv`) | Cleaned (`data/processed/amazon-products-cleaned.csv`) | Resolution |
| :--- | :--- | :--- | :---: |
| **Physical Lines** | 1,002 lines (Row 320 split by `\n`) | **1,001 lines** (1 header + 1,000 data rows) |  Resolved |
| **Total Columns** | 55 columns | **60 columns** (3 dead dropped, 8 structured added) |  Expanded |
| **Category Parsing** | Serialized JSON list `["Clothing...", ...]` | **7 structured columns** (`level_1` to `level_4`, `leaf`, `path`, `depth`) |  Direct SQL/BI |
| **Quoted Prices** | 852 rows had escaped triple quotes (`"""57.79"""`) | **0 quoted prices**; 100% clean decimal floats |  Castable |
| **Scientific Notation** | 177 initial / 139 final prices in sci notation (`1.795e+01`) | Standardized 2-decimal floats (`17.95`) |  Normalized |
| **Redacted Sellers** | 801 sellers masked with `█` (`Ama███.co███`) | **0 redacted sellers**; 901 restored using buybox |  Unmasked |
| **BiDi Control Marks** | 300+ occurrences of `\u200e` & `\u200f` in 7 columns | **0 BiDi marks** across all columns |  Stripped |
| **Date Format** | Mixed text (`February 17, 2022`, `25 November 2023`) | **100% ISO-8601 `YYYY-MM-DD`** (921 valid dates) |  Standardized |
| **Description Noise** | 25 rows with `.aplus-v2` CSS & JS code in description | Stripped CSS/JS stylesheets & unescaped HTML entities |  Clean Text |
| **Domain Hostnames** | 826 rows had `https://` prefix & `/` suffix | Normalized to clean hostnames (`www.amazon.com`) |  Categorical |
| **Discount Metric** | 5 fragmented formats (%, ints, INR, multiline) | Clean numeric **`discount_percentage`** float column |  Calculated |
| **Null Sentinels** | Inconsistent literal string `'null'` vs empty string | Standard empty string `""` across all fields |  SQL-Safe |

---

## 📋 Cleaned Dataset Schema (60 Columns)

| # | Column Name | Data Type | Null Count (%) | Description |
| :-: | :--- | :--- | :-: | :--- |
| 1 | `timestamp` | `TIMESTAMP` | 0 (0.0%) | Scrape timestamp (ISO-8601) |
| 2 | `title` | `VARCHAR` | 0 (0.0%) | Full product title |
| 3 | `seller_name` | `VARCHAR` | 74 (7.4%) | Unmasked merchant name (restored via buybox) |
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

### Prerequisites
```bash
pip install pandas numpy reportlab
```

### 1. Run Data Cleaning & Category Expansion Pipeline
```bash
python src/clean_amazon_products.py
```
Reads `data/raw/amazon-products.csv` and outputs `data/processed/amazon-products-cleaned.csv`.

### 2. Run Category Performance Analytics
```bash
python src/analyze_category_performance.py
```
Outputs category catalog share, customer ratings, review volume distributions, and strategic assessments.
