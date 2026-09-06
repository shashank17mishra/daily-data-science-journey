import pytest
import numpy as np
from analysis import generate_synthetic_sales, analyze_sales_summary

def test_generate_synthetic_sales():
    df = generate_synthetic_sales(records=50, seed=123)
    assert len(df) == 50
    assert "total_revenue" in df.columns
    assert np.isclose(df["total_revenue"], df["quantity"] * df["unit_price"]).all()

def test_analyze_sales_summary():
    df = generate_synthetic_sales(records=50, seed=123)
    summary = analyze_sales_summary(df)
    assert len(summary) > 0
    assert "gross_revenue" in summary.columns
