"""
Portfolio Project 1: Sales Data Analysis Pipeline.
Generates synthetic sales data and computes key financial KPIs.
"""
import pandas as pd
import numpy as np

def generate_synthetic_sales(records: int = 100, seed: int = 42) -> pd.DataFrame:
    """Generates synthetic transactional sales data for demonstration."""
    np.random.seed(seed)
    categories = ["Electronics", "Clothing", "Home & Kitchen", "Books"]

    df = pd.DataFrame({
        "order_id": [f"ORD-{1000 + i}" for i in range(records)],
        "category": np.random.choice(categories, size=records),
        "quantity": np.random.randint(1, 5, size=records),
        "unit_price": np.round(np.random.uniform(15.0, 300.0, size=records), 2)
    })
    df["total_revenue"] = np.round(df["quantity"] * df["unit_price"], 2)
    return df

def analyze_sales_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Computes revenue summary by product category."""
    summary = df.groupby("category").agg(
        total_orders=("order_id", "count"),
        total_items_sold=("quantity", "sum"),
        gross_revenue=("total_revenue", "sum"),
        average_order_value=("total_revenue", "mean")
    ).reset_index()
    return summary.sort_values(by="gross_revenue", ascending=False)
