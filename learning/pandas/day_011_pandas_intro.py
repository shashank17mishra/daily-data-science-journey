"""
Day 011: Pandas DataFrame Fundamentals & GroupBy Aggregations.
"""
import pandas as pd

def calculate_department_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Group employee DataFrame by department and calculates aggregate metrics."""
    required_cols = {"department", "salary", "bonus"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"DataFrame must contain columns: {required_cols}")

    aggregated = df.groupby("department").agg(
        total_employees=("salary", "count"),
        avg_salary=("salary", "mean"),
        max_bonus=("bonus", "max")
    ).reset_index()

    return aggregated
