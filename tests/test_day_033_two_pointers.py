import pytest
from learning.dsa.day_033_two_pointers import two_sum_sorted, max_area

def test_two_sum_sorted_success():
    assert two_sum_sorted([2, 7, 11, 15], 9) == (1, 2)
    assert two_sum_sorted([2, 3, 4], 6) == (1, 3)
    assert two_sum_sorted([-1, 0], -1) == (1, 2)

def test_two_sum_sorted_no_solution():
    assert two_sum_sorted([1, 2, 3, 4], 10) == (-1, -1)
    assert two_sum_sorted([], 5) == (-1, -1)
    assert two_sum_sorted([5], 5) == (-1, -1)

def test_max_area_success():
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert max_area([1, 1]) == 1
    assert max_area([4, 3, 2, 1, 4]) == 16

def test_max_area_edge_cases():
    assert max_area([]) == 0
    assert max_area([1]) == 0
    assert max_area([1, 2, 1]) == 2
