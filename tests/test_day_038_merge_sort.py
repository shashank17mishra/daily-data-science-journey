"""Unit tests for Merge Sort implementation and inversion counting."""

import pytest
from learning.dsa.day_038_merge_sort import count_inversions, merge_sort


def test_merge_sort_basic():
    arr = [38, 27, 43, 3, 9, 82, 10]
    expected = [3, 9, 10, 27, 38, 43, 82]
    assert merge_sort(arr) == expected


def test_merge_sort_edge_cases():
    assert merge_sort([]) == []
    assert merge_sort([42]) == [42]
    assert merge_sort([1, 1, 1, 1]) == [1, 1, 1, 1]


def test_merge_sort_already_sorted():
    arr = [1, 2, 3, 4, 5]
    assert merge_sort(arr) == [1, 2, 3, 4, 5]


def test_merge_sort_reverse_sorted():
    arr = [5, 4, 3, 2, 1]
    assert merge_sort(arr) == [1, 2, 3, 4, 5]


def test_merge_sort_negative_and_floats():
    arr = [-3.5, 0.0, -10.2, 5.1, 2.0]
    assert merge_sort(arr) == [-10.2, -3.5, 0.0, 2.0, 5.1]


def test_merge_sort_reverse_option():
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    assert merge_sort(arr, reverse=True) == [9, 6, 5, 4, 3, 2, 1, 1]


def test_merge_sort_with_key():
    words = ["python", "is", "awesome", "a"]
    sorted_by_length = merge_sort(words, key=len)
    assert sorted_by_length == ["a", "is", "python", "awesome"]


def test_merge_sort_stability():
    class Item:
        def __init__(self, key: int, name: str):
            self.key = key
            self.name = name

    items = [Item(2, "first_2"), Item(1, "first_1"), Item(2, "second_2")]
    sorted_items = merge_sort(items, key=lambda x: x.key)
    names = [item.name for item in sorted_items]
    assert names == ["first_1", "first_2", "second_2"]


def test_count_inversions_basic():
    arr = [2, 4, 1, 3, 5]
    sorted_arr, count = count_inversions(arr)
    assert sorted_arr == [1, 2, 3, 4, 5]
    assert count == 3


def test_count_inversions_sorted_and_reversed():
    _, inv_sorted = count_inversions([1, 2, 3, 4, 5])
    assert inv_sorted == 0

    _, inv_reversed = count_inversions([5, 4, 3, 2, 1])
    assert inv_reversed == 10
