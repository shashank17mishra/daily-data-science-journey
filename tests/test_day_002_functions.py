import pytest
from learning.python.day_002_functions import calculate_summary_stats

def test_calculate_summary_stats():
    res = calculate_summary_stats(10, 20, 30, 40, dataset_name="sales", analyst="Bob")
    assert res["count"] == 4
    assert res["min"] == 10.0
    assert res["max"] == 40.0
    assert res["mean"] == 25.0
    assert res["dataset_name"] == "sales"
    assert res["analyst"] == "Bob"

def test_calculate_summary_stats_empty():
    with pytest.raises(ValueError):
        calculate_summary_stats()
