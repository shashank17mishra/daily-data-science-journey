"""
Day 012: Data Cleaning Pipeline with Missing Value Imputation and Deduplication.
"""
import pandas as pd

def clean_customer_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans messy customer DataFrame:
    1. Removes duplicate rows based on customer_id.
    2. Fills missing age values with median age.
    3. Standardizes email addresses to lowercase.
    """
    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates(subset=["customer_id"])

    if "age" in cleaned.columns:
        median_age = cleaned["age"].median()
        cleaned["age"] = cleaned["age"].fillna(median_age)

    if "email" in cleaned.columns:
        cleaned["email"] = cleaned["email"].astype(str).str.lower().str.strip()

    return cleaned
