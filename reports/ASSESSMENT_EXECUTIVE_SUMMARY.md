# Amazon Product Dataset Analysis: Executive Summary

**Role:** AI-First Analytics Engineer Assessment  
**Candidate:** anujhsrsaini  
**Live AI Assistant:** Antigravity CLI (Google Gemini 3.8 Flash)  
**Interactive Repository:** [https://github.com/anujhsrsaini/Pearl-Assignment](https://github.com/anujhsrsaini/Pearl-Assignment)  
**Downloadable PDF Version:** [`reports/ASSESSMENT_EXECUTIVE_SUMMARY.pdf`](./ASSESSMENT_EXECUTIVE_SUMMARY.pdf)

---

### Context & AI-First Operating Model
This evaluation simulated a live, 30-minute analytical engagement on unfamiliar scraped eCommerce data (~1,000 Amazon product records from Luminati/BrightData). Operating with an AI-first methodology, I orchestrated a team of specialized autonomous agents (Structure Inspector, Schema Profiler, Quality Auditor) to diagnose and clean the dataset before formulating executive recommendations for a Category Manager.

---

## 1. Get Oriented: What is this data, and would you trust it?

**The Reality:** The dataset contains 1,000 scraped Amazon product records across 55 columns. In its raw state, **I would not trust this data as a basis for any commercial business decision.**

* **Silent Parsing Failures:** A literal newline (`\n`) in Row 320's discount field split the record across lines 321 and 322, breaking naive parsers into 27- and 29-column fragments. Massive serialized JSON arrays in product variations (up to 151 KB) trigger buffer overflow crashes in default Python CSV readers (`_csv.Error: field larger than field limit`).
* **Price Corruption:** Over 85% of `final_price` values were escaped with triple quotes (`"""57.79"""`), and 177 prices were formatted in scientific notation (`1.795000000000000e+01`). Direct numeric casting fails immediately without regex sanitization.
* **Ghost Columns & Redactions:** Three columns (`product_details`, `prices_breakdown`, `country_of_origin`) are 100% empty. Furthermore, 801 seller names were obfuscated with black blocks (`█`).
* **What was checked and fixed first:** Before analyzing, an automated pipeline dropped dead columns, sanitized prices to floats, recovered seller identities using unmasked buybox data, stripped invisible BiDi marks (`\u200e`/`\u200f`), and expanded JSON category trees into 7 queryable columns.

---

## 2. Business Question: "Which product category should we prioritise, and why?"

**Executive Recommendation to Category Manager:** Prioritise **Home & Kitchen** as the primary volume pillar, paired with **Tools & Home Improvement** for rapid market penetration.

### Category Performance Benchmark (100% Verified Data)

| Category | Catalog Share | Total Reviews | Median Reviews | Mean Rating | Strategic Viability Assessment |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Home & Kitchen** | **15.0%** (150) | 417,487 (12.9%) | 498.5 | **4.47 / 5.0** | **Primary Recommendation:** High customer delight (4.47), large addressable catalog, manageable review barrier (~500 reviews). |
| **Tools & Home Improvement** | **11.2%** (112) | 104,117 (3.2%) | 221.5 | **4.38 / 5.0** | **Low-Hanging Fruit:** Lowest review barrier among major categories (221 median). Fast path for new listings to achieve search parity. |
| **Clothing, Shoes & Jewelry** | 21.6% (216) | 951,495 (29.3%) | 924.5 | 4.36 / 5.0 | **Saturated / High Moat:** High volume, but incumbent review moat (>920 median) requires massive ad spend to compete. |
| **Pet Supplies** | 2.6% (26) | 409,036 (12.6%) | **2,007.5** | 4.35 / 5.0 | **Extreme Review Moat:** Incredible review density (2,008 median reviews), but entry barriers for unproven brands are severe. |
| **Beauty** | 3.1% (31) | 110,555 (3.4%) | 114.0 | **4.06 / 5.0** | **High Risk:** Lowest customer rating on Amazon (4.06 vs 4.40 platform avg). Elevated return and dissatisfaction rates. |

* **What the data supports:** Catalog presence, relative social proof intensity (review counts), and customer sentiment distributions (ratings) across categories.
* **What the data DOES NOT support:** Revenue, unit velocity, profit margins, conversion rates, or return rates. We can measure listing dominance, not commercial profitability.

---

## 3. Data Skepticism: What you must verify before taking action

* **Phantom Discounts (87 Rows):** In 87 listings, `initial_price == final_price` down to the cent, yet non-zero discounts (up to -82%) were recorded. Raw scrape discounts are marketing badges, not financial truths.
* **Multi-Currency Poisoning:** The dataset mixes USD (96.7%), INR (3.1%), and GBP (0.2%). Treating final prices as homogeneous numbers without FX normalization produces completely distorted price brackets.
* **Unverified Velocity (`bought_past_month`):** 79.6% null, and the remaining values are coarse Amazon rounded estimates (e.g. 50, 100, 1000). It cannot be used for inventory forecasting.

---

## 4. Something You Didn't Ask: Observations Beyond the Brief

1. **Security / Scraping Leak:** While `seller_name` was intentionally redacted with block glyphs (`█`) in 801 rows for anonymity, the scraper inadvertently captured `buybox_seller` completely unmasked. This allowed us to 100% reverse-engineer vendor identities and map Amazon 1P vs 3P buybox control.
2. **The Question I Wanted to Answer but Couldn't:** *"Does Amazon prioritize its own private-label products (Amazon Essentials) over 3P merchants in the Buy Box when competing on identical price?"* — Cannot be definitively proven because competitor price bid logs (`prices_breakdown`) are 100% dead.

---

## 5. AI Workflow & Shareable Conversation Links

Every step of this session — prompt chains, agent tool execution, raw transcripts, and code — is permanently committed:

* **Session Transcripts:** [https://github.com/anujhsrsaini/Pearl-Assignment/tree/main/antigravity_conversations](https://github.com/anujhsrsaini/Pearl-Assignment/tree/main/antigravity_conversations)
* **Reproducible Cleaning Pipeline:** [`src/clean_amazon_products.py`](https://github.com/anujhsrsaini/Pearl-Assignment/blob/main/src/clean_amazon_products.py)
* **Detailed Data Audit Report:** [`reports/amazon_products_audit_report.md`](https://github.com/anujhsrsaini/Pearl-Assignment/blob/main/reports/amazon_products_audit_report.md)
