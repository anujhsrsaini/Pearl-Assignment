# Business Performance Analysis: Category Engagement & Customer Satisfaction

**Target Question:** *Which product categories dominate Amazon in catalog presence, and how do customer engagement (review volume) and customer satisfaction (ratings) vary across top-level categories?*  
**Data Integrity Standard:** Built **strictly on 100% verified, non-null data** (`categories`, `rating`, and `reviews_count` across all 1,000 products in [`amazon-products-cleaned.csv`](./amazon-products-cleaned.csv)).  
**Analysis Sample:** 1,000 / 1,000 Products (0 exclusions, 0 currency conversions required).

---

## 1. Executive Summary

1. **Catalog Concentration (Top 3 = 47.8% of Catalog):**
   - Three categories account for nearly half of Amazon's catalog: **Clothing, Shoes & Jewelry (21.6%)**, **Home & Kitchen (15.0%)**, and **Tools & Home Improvement (11.2%)**.
2. **Review Moat & Social Proof Disparity:**
   - **Pet Supplies** and **Electronics** punch drastically above their weight:
     - `Pet Supplies` commands **12.6% of all platform reviews** with only **2.6% of catalog products** (median reviews: **2,007.5** vs platform median of 461.5).
     - `Clothing, Shoes & Jewelry` commands **29.3% of all platform reviews** (951,495 total reviews).
   - In contrast, `Tools & Home Improvement` has an **exceptionally low review barrier** (median reviews: **221.5**, capturing only 3.2% of reviews despite 11.2% catalog presence).
3. **Customer Satisfaction Extremes:**
   - **Highest Rated:** `Office Products` (mean: **4.60 / 5.0**, median: **4.70**) and `Arts, Crafts & Sewing` (mean: **4.60 / 5.0**).
   - **Lowest Rated / Highest Friction:** `Beauty` is the harshest category with a mean rating of **4.06 / 5.0** (well below platform average of 4.40), indicating higher customer dissatisfaction or product expectation mismatch.

---

## 2. Category Performance Benchmark Table

| Root Category | Products (Count) | Catalog Share (%) | Total Reviews | Review Share (%) | Median Reviews | Mean Reviews | Mean Rating | Rating Std |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Clothing, Shoes & Jewelry** | 216 | 21.6% | 951,495 | 29.3% | 924.5 | 4,405.1 | **4.36** | 0.23 |
| **Home & Kitchen** | 150 | 15.0% | 417,487 | 12.9% | 498.5 | 2,783.2 | **4.47** | 0.24 |
| **Tools & Home Improvement** | 112 | 11.2% | 104,117 | 3.2% | 221.5 | 929.6 | **4.38** | 0.34 |
| **Sports & Outdoors** | 78 | 7.8% | 108,471 | 3.3% | 226.5 | 1,390.7 | **4.43** | 0.36 |
| **Electronics** | 75 | 7.5% | 430,886 | 13.3% | 356.0 | 5,745.1 | **4.32** | 0.40 |
| **Automotive** | 56 | 5.6% | 47,072 | 1.4% | 158.5 | 840.6 | **4.31** | 0.34 |
| **Office Products** | 45 | 4.5% | 151,604 | 4.7% | 716.0 | 3,369.0 | **4.60** | 0.22 |
| **Health & Household** | 33 | 3.3% | 127,016 | 3.9% | 1,047.0 | 3,849.0 | **4.54** | 0.23 |
| **Beauty** | 31 | 3.1% | 110,555 | 3.4% | 114.0 | 3,566.3 | **4.06** | 0.39 |
| **Cell Phones & Accessories**| 27 | 2.7% | 59,531 | 1.8% | 488.0 | 2,204.9 | **4.29** | 0.33 |
| **Arts, Crafts & Sewing** | 27 | 2.7% | 33,733 | 1.0% | 260.0 | 1,249.4 | **4.60** | 0.17 |
| **Pet Supplies** | 26 | 2.6% | 409,036 | 12.6% | **2,007.5** | **15,732.2**| **4.35** | 0.26 |
| **Patio, Lawn & Garden** | 24 | 2.4% | 40,104 | 1.2% | 115.5 | 1,671.0 | **4.35** | 0.36 |
| **Beauty & Personal Care** | 23 | 2.3% | 127,712 | 3.9% | 486.0 | 5,552.7 | **4.43** | 0.24 |
| **Toys & Games** | 21 | 2.1% | 51,006 | 1.6% | 630.0 | 2,428.9 | **4.52** | 0.22 |
| **Industrial & Scientific** | 17 | 1.7% | 12,028 | 0.4% | 353.0 | 707.5 | **4.29** | 0.57 |
| **Others (12 categories)** | 49 | 4.9% | 67,285 | 2.1% | 551.0 | 1,373.2 | **4.51** | 0.24 |
| **PLATFORM TOTAL / OVERALL** | **1,000** | **100.0%** | **3,248,806** | **100.0%** | **461.5** | **3,248.8** | **4.40** | **0.31** |

---

## 3. Strategic Business Takeaways

### A. The "Review Moat" Hierarchy
- **High-Moat Categories (Hard for New Sellers):**
  - `Pet Supplies` (Median: 2,008 reviews) and `Clothing` (Median: 925 reviews). Established incumbents possess massive social proof moats. Entering here requires heavy initial review generation campaigns.
- **Low-Barrier Categories (Easiest for New Entrants):**
  - `Tools & Home Improvement` (Median: 221 reviews) and `Automotive` (Median: 158 reviews). A new product with just 150–200 high-quality reviews can immediately compete on par with established listings.

### B. Customer Satisfaction & Risk Profile
- **Low Returns / High Delight:** `Office Products` (4.60 rating, std 0.22) and `Arts, Crafts & Sewing` (4.60 rating, std 0.17). Low variance indicates consistent customer satisfaction and lower return/complaint rates.
- **High Friction / High Returns:** `Beauty` (4.06 rating, std 0.39) and `Electronics` (4.32 rating, std 0.40). These categories carry the highest risk of negative customer feedback, likely driven by subjective efficacy (skincare/cosmetics) and technical defect/compatibility issues (electronics).
