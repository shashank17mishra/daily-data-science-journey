import pytest
from learning.python.day_007_oop import Dataset, NumericDataset

def test_dataset_base():
    ds = Dataset("metrics", [10, 20, 30])
    assert ds.size == 3
    assert ds.summary() == "Dataset 'metrics' containing 3 items."

def test_numeric_dataset():
    num_ds = NumericDataset("temperatures", [20.0, 25.0, 30.0])
    assert num_ds.size == 3
    assert num_ds.mean() == 25.0

def test_numeric_dataset_empty():
    empty_ds = NumericDataset("empty", [])
    with pytest.raises(ValueError):
        empty_ds.mean()
