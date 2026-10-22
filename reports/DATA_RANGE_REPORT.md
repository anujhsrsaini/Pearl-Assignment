# Amazon Products Dataset - Timestamp Range Report

## 1. Overview

This document summarizes the analysis of the `timestamp` column in [`amazon-products.csv`](file:///D:/Anuj/Pearl-ASsignment/amazon-products.csv).

| Metric | Value |
| :--- | :--- |
| **Source File** | `amazon-products.csv` |
| **Total Rows** | 1,000 |
| **Column Analyzed** | `timestamp` |
| **Missing / Null Values** | 0 (100% complete) |
| **Unique Timestamps** | 141 distinct dates |
| **Format** | `YYYY-MM-DD 00:00:00.000` |

---

## 2. Date Range

* **Earliest Timestamp (Min):** `2022-09-06 00:00:00.000` (September 6, 2022)
* **Latest Timestamp (Max):** `2024-07-10 00:00:00.000` (July 10, 2024)
* **Total Time Span:** 673 calendar days (~1 year, 10 months, 4 days)

---

## 3. Distribution

### By Year

| Year | Record Count | Percentage |
| :--- | :--- | :--- |
| **2022** | 129 | 12.9% |
| **2023** | 498 | 49.8% |
| **2024** | 373 | 37.3% |
| **Total** | **1,000** | **100.0%** |

### By Month

| Year-Month | Record Count |
| :--- | :--- |
| **2022-09** | 78 |
| **2022-10** | 51 |
| **2023-04** | 3 |
| **2023-05** | 42 |
| **2023-07** | 2 |
| **2023-08** | 325 |
| **2023-09** | 47 |
| **2023-10** | 69 |
| **2023-11** | 10 |
| **2024-01** | 89 |
| **2024-02** | 30 |
| **2024-03** | 37 |
| **2024-04** | 72 |
| **2024-05** | 55 |
| **2024-06** | 53 |
| **2024-07** | 37 |

---

## 4. Key Observations

1. **No Timestamp Gaps / Missing Data**: All 1,000 records contain a valid date string.
2. **Normalized Time Components**: Every timestamp entry is normalized to midnight (`00:00:00.000`).
3. **Data Concentration**: August 2023 represents the highest volume of records (325 rows, or 32.5% of the entire dataset).
