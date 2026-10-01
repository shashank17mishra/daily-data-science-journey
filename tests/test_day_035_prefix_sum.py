import pytest
from learning.dsa.day_035_prefix_sum import PrefixSum1D, PrefixSum2D

def test_prefix_sum_1d_basic():
    arr = [1, 2, 3, 4, 5]
    ps = PrefixSum1D(arr)
    assert ps.query(0, 2) == 6  # 1 + 2 + 3
    assert ps.query(1, 3) == 9  # 2 + 3 + 4
    assert ps.query(0, 4) == 15 # 1 + 2 + 3 + 4 + 5
    assert ps.query(2, 2) == 3  # Single element

def test_prefix_sum_1d_floats_and_negatives():
    arr = [-1.5, 2.5, 0.0, -3.0]
    ps = PrefixSum1D(arr)
    assert ps.query(0, 1) == 1.0
    assert ps.query(1, 3) == -0.5

def test_prefix_sum_1d_edge_cases():
    # Empty array
    ps_empty = PrefixSum1D([])
    with pytest.raises(ValueError):
        ps_empty.query(0, 0)

    # Out of bounds
    ps = PrefixSum1D([1, 2, 3])
    with pytest.raises(IndexError):
        ps.query(-1, 2)
    with pytest.raises(IndexError):
        ps.query(0, 3)
    
    # Invalid range (left > right)
    with pytest.raises(ValueError):
        ps.query(2, 1)

def test_prefix_sum_2d_basic():
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    ps = PrefixSum2D(matrix)
    # Full matrix
    assert ps.query(0, 0, 2, 2) == 45
    # Single element
    assert ps.query(1, 1, 1, 1) == 5
    # Subgrid
    assert ps.query(0, 1, 1, 2) == 16  # 2 + 3 + 5 + 6
    assert ps.query(1, 0, 2, 1) == 24  # 4 + 5 + 7 + 8

def test_prefix_sum_2d_edge_cases():
    # Empty matrix
    ps_empty = PrefixSum2D([])
    with pytest.raises(ValueError):
        ps_empty.query(0, 0, 0, 0)

    matrix = [
        [1, 2],
        [3, 4]
    ]
    ps = PrefixSum2D(matrix)
    
    # Out of bounds
    with pytest.raises(IndexError):
        ps.query(-1, 0, 1, 1)
    with pytest.raises(IndexError):
        ps.query(0, 0, 2, 1)
    
    # Invalid range (r1 > r2 or c1 > c2)
    with pytest.raises(IndexError):
        ps.query(1, 0, 0, 1)
