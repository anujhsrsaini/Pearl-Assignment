# Seller Columns Verification Report

## 1. Overview

This document provides verification and quality analysis of seller-related columns in [`amazon-products.csv`](file:///D:/Anuj/Pearl-ASsignment/amazon-products.csv), specifically comparing `seller_name` and `seller_id`, along with the related `buybox_seller` column.

---

## 2. Comparison Matrix

| Metric | `seller_name` | `seller_id` | `buybox_seller` |
| :--- | :--- | :--- | :--- |
| **Total Rows** | 1,000 | 1,000 | 1,000 |
| **Masked / Redacted Rows** | **801 (80.1%)** | **0 (0.0%)** | **0 (0.0%)** |
| **Missing / Null Rows** | **174 (17.4%)** | **0 (0.0%)** | **74 (7.4%)** |
| **Clean / Usable Rows** | **25 (2.5%)** | **1,000 (100.0%)** | **926 (92.6%)** |
| **Unique Values** | 569 | 671 | 658 |
| **Primary Data Format** | Redacted strings with `█` | Alphanumeric Merchant ID | Human-readable seller name |
| **Suitability for Analysis** | ❌ Unusable |  Ideal (Primary Key) |  Usable for Display |

---

## 3. Detailed Findings

### A. `seller_name` (Heavily Redacted)
- **Masking Character:** Uses Unicode full-block characters (`█` / `\u2588`) to redact partial seller names.
  - Examples: `Ama███.co███`, `RK ███ld ███oco█████████`, `Orv███tor███`.
- **Null Rate:** 174 rows (17.4%) are completely missing.
- **Combined Invalidation:** **97.5%** of rows are either masked or null, leaving only 25 usable rows.

### B. `seller_id` (Clean & Complete)
- **Completeness:** 100% complete (0 nulls across 1,000 rows).
- **Format:** Standard Amazon Merchant IDs (12 to 14 alphanumeric characters).
  - Example: `ATVPDKIKX0DER` corresponds to Amazon.com retail.
- **Uniqueness:** 671 distinct seller IDs across 1,000 products.
- **No Masking:** Zero block characters or redaction artifacts.

### C. `buybox_seller` (Unmasked Name Alternative)
- **Completeness:** 92.6% populated (74 nulls).
- **Masking:** 0% masked.
- Contains the clean, human-readable seller names that directly correspond to the masked values in `seller_name`.

---

## 4. Sample Row-Level Mappings

| Row Index | Masked `seller_name` | Clean `seller_id` | Unmasked `buybox_seller` |
| :--- | :--- | :--- | :--- |
| **0** | `Orv███tor███` | `A2NEM58BFPMEIL` | `Orva Stores` |
| **1** | `Ama███.co███` | `ATVPDKIKX0DER` | `Amazon.com` |
| **2** | `Twi███uxe███` | `A32T2M1BDX55RN` | `Twinsluxes` |
| **3** | `Cit███ran███Dir██████` | `A1J9XHX48UC47C` | `City Brands Direct` |
| **4** | `PRA███ EN███PRI███` | `A2I00EBEBYMKDS` | `PRANTH ENTERPRISE` |

---

## 5. Recommendations

1. **Primary Identifier / Join Key:** Use **`seller_id`** for all entity resolution, aggregations, filtering, and cross-table joins.
2. **Display / Labeling:** Do not use `seller_name`. If human-readable seller names are required for dashboards or reports, use **`buybox_seller`** as the primary source for names.
