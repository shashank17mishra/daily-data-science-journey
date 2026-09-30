import pytest
from learning.dsa.day_034_sliding_window import (
    max_subarray_sum_fixed,
    min_subarray_len_target,
    longest_substring_k_distinct,
)


def test_max_subarray_sum_fixed_basic():
    arr = [2, 1, 5, 1, 3, 2]
    k = 3
    assert max_subarray_sum_fixed(arr, k) == 9


def test_max_subarray_sum_fixed_negative():
    arr = [-1, -2, -3, -4, -5]
    k = 2
    assert max_subarray_sum_fixed(arr, k) == -3


def test_max_subarray_sum_fixed_k_equals_length():
    arr = [1, 2, 3, 4]
    assert max_subarray_sum_fixed(arr, 4) == 10


def test_max_subarray_sum_fixed_invalid_k():
    with pytest.raises(ValueError):
        max_subarray_sum_fixed([1, 2, 3], 0)
    with pytest.raises(ValueError):
        max_subarray_sum_fixed([1, 2, 3], 4)


def test_min_subarray_len_target_basic():
    arr = [2, 3, 1, 2, 4, 3]
    target = 7
    assert min_subarray_len_target(target, arr) == 2


def test_min_subarray_len_target_no_solution():
    arr = [1, 1, 1, 1]
    target = 10
    assert min_subarray_len_target(target, arr) == 0


def test_min_subarray_len_target_single_element():
    arr = [1, 4, 4]
    target = 4
    assert min_subarray_len_target(target, arr) == 1


def test_min_subarray_len_target_invalid_target():
    with pytest.raises(ValueError):
        min_subarray_len_target(0, [1, 2, 3])


def test_longest_substring_k_distinct_basic():
    s = "eceba"
    k = 2
    assert longest_substring_k_distinct(s, k) == 3


def test_longest_substring_k_distinct_all_unique():
    s = "araaci"
    k = 2
    assert longest_substring_k_distinct(s, k) == 4


def test_longest_substring_k_distinct_edge_cases():
    assert longest_substring_k_distinct("", 2) == 0
    assert longest_substring_k_distinct("abc", 0) == 0
    assert longest_substring_k_distinct("aaaa", 1) == 4
    assert longest_substring_k_distinct("abc", 5) == 3
