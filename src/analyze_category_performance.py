import os
import json
import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

DATA_PATH = os.path.join(REPO_ROOT, "data", "processed", "amazon-products-cleaned.csv")
REPORT_PATH = os.path.join(REPO_ROOT, "reports", "BUSINESS_INSIGHTS_CATEGORY_PERFORMANCE.md")

def analyze():
    print(f"Loading cleaned dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH, keep_default_na=False)
    print(f"Loaded {len(df)} products.")

    # Aggregations by category_level_1
    agg = df.groupby('category_level_1').agg(
        catalog_share=('asin', 'count'),
        mean_rating=('rating', 'mean'),
        median_rating=('rating', 'median'),
        rating_std=('rating', 'std'),
        total_reviews=('reviews_count', 'sum'),
        mean_reviews=('reviews_count', 'mean'),
        median_reviews=('reviews_count', 'median'),
        q25_reviews=('reviews_count', lambda x: np.percentile(x, 25)),
        q75_reviews=('reviews_count', lambda x: np.percentile(x, 75))
    ).reset_index()

    agg['catalog_pct'] = (agg['catalog_share'] / len(df) * 100).round(1)
    agg['review_share_pct'] = (agg['total_reviews'] / df['reviews_count'].sum() * 100).round(1)
    agg['mean_rating'] = agg['mean_rating'].round(2)
    agg['mean_reviews'] = agg['mean_reviews'].round(1)
    agg['median_reviews'] = agg['median_reviews'].round(1)

    agg = agg.sort_values(by='catalog_share', ascending=False)
    print("\nTop 10 Categories by Catalog Share:")
    print(agg[['category_level_1', 'catalog_share', 'catalog_pct', 'mean_rating', 'median_reviews', 'review_share_pct']].head(10).to_string(index=False))

    return agg

if __name__ == '__main__':
    analyze()
