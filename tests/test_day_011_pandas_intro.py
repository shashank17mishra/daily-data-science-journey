import pandas as pd
import pytest
from learning.pandas.day_011_pandas_intro import calculate_department_kpis

def test_calculate_department_kpis():
    data = {
        "department": ["Engineering", "Engineering", "Sales", "Sales"],
        "salary": [100000, 120000, 80000, 90000],
        "bonus": [15000, 20000, 10000, 12000]
    }
    df = pd.DataFrame(data)
    res = calculate_department_kpis(df)

    assert len(res) == 2
    eng_row = res[res["department"] == "Engineering"].iloc[0]
    assert eng_row["total_employees"] == 2
    assert eng_row["avg_salary"] == 110000.0
    assert eng_row["max_bonus"] == 20000
