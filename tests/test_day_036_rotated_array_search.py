"""Unit tests for binary search and rotated array algorithms."""

import pytest
from learning.dsa.day_036_rotated_array_search import (
    binary_search,
    find_min_rotated_array,
    search_rotated_array,
)


class TestBinarySearch:
    """Tests for standard binary search implementation."""

    def test_found_element_middle(self):
        assert binary_search([1, 3, 5, 7, 9], 5) == 2

    def test_found_element_boundaries(self):
        arr = [2, 4, 6, 8, 10]
        assert binary_search(arr, 2) == 0
        assert binary_search(arr, 10) == 4

    def test_not_found(self):
        assert binary_search([1, 3, 5, 7, 9], 4) == -1

    def test_empty_array(self):
        assert binary_search([], 5) == -1

    def test_single_element_found(self):
        assert binary_search([42], 42) == 0

    def test_single_element_not_found(self):
        assert binary_search([42], 7) == -1


class TestSearchRotatedArray:
    """Tests for searching in a rotated sorted array."""

    def test_search_typical_rotation(self):
        nums = [4, 5, 6, 7, 0, 1, 2]
        assert search_rotated_array(nums, 0) == 4
        assert search_rotated_array(nums, 4) == 0
        assert search_rotated_array(nums, 2) == 6

    def test_search_not_found(self):
        nums = [4, 5, 6, 7, 0, 1, 2]
        assert search_rotated_array(nums, 3) == -1

    def test_search_unrotated_array(self):
        nums = [0, 1, 2, 4, 5, 6, 7]
        assert search_rotated_array(nums, 5) == 4

    def test_search_single_element(self):
        assert search_rotated_array([1], 1) == 0
        assert search_rotated_array([1], 0) == -1

    def test_search_two_elements(self):
        assert search_rotated_array([3, 1], 1) == 1
        assert search_rotated_array([3, 1], 3) == 0
        assert search_rotated_array([3, 1], 2) == -1

    def test_search_empty_array(self):
        assert search_rotated_array([], 1) == -1


class TestFindMinRotatedArray:
    """Tests for finding minimum in rotated sorted array."""

    def test_find_min_typical_rotation(self):
        assert find_min_rotated_array([3, 4, 5, 1, 2]) == 1
        assert find_min_rotated_array([4, 5, 6, 7, 0, 1, 2]) == 0

    def test_find_min_unrotated(self):
        assert find_min_rotated_array([11, 13, 15, 17]) == 11

    def test_find_min_single_element(self):
        assert find_min_rotated_array([5]) == 5

    def test_find_min_two_elements(self):
        assert find_min_rotated_array([2, 1]) == 1
        assert find_min_rotated_array([1, 2]) == 1

    def test_find_min_empty_raises_value_error(self):
        with pytest.raises(ValueError, match="Cannot find minimum"):
            find_min_rotated_array([])
