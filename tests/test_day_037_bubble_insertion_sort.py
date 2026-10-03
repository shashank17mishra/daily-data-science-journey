import pytest
from learning.dsa.day_037_bubble_insertion_sort import bubble_sort, insertion_sort


@pytest.mark.parametrize("sort_func", [bubble_sort, insertion_sort])
def test_empty_and_single_element(sort_func):
    """Test that empty and single-element lists are handled correctly."""
    # Empty list
    res_empty = sort_func([])
    assert res_empty["sorted_list"] == []
    assert res_empty["comparisons"] == 0

    # Single element
    res_single = sort_func([42])
    assert res_single["sorted_list"] == [42]
    assert res_single["comparisons"] == 0


@pytest.mark.parametrize("sort_func", [bubble_sort, insertion_sort])
def test_already_sorted(sort_func):
    """Test behavior and metrics on an already sorted list."""
    arr = [1, 2, 3, 4, 5]
    res = sort_func(arr.copy())
    assert res["sorted_list"] == [1, 2, 3, 4, 5]
    
    # For bubble sort, optimized version should stop after 1 pass (n-1 comparisons, 0 swaps)
    if sort_func.__name__ == "bubble_sort":
        assert res["comparisons"] == 4
        assert res["swaps"] == 0
    # For insertion sort, it should do n-1 comparisons and 0 shifts
    elif sort_func.__name__ == "insertion_sort":
        assert res["comparisons"] == 4
        assert res["shifts"] == 0


@pytest.mark.parametrize("sort_func", [bubble_sort, insertion_sort])
def test_reverse_sorted(sort_func):
    """Test sorting a reverse-ordered list."""
    arr = [5, 4, 3, 2, 1]
    res = sort_func(arr.copy())
    assert res["sorted_list"] == [1, 2, 3, 4, 5]
    
    if sort_func.__name__ == "bubble_sort":
        # Worst case bubble sort swaps: n*(n-1)/2 = 10
        assert res["swaps"] == 10
    elif sort_func.__name__ == "insertion_sort":
        # Worst case insertion sort shifts: n*(n-1)/2 = 10
        assert res["shifts"] == 10


@pytest.mark.parametrize("sort_func", [bubble_sort, insertion_sort])
def test_duplicates_and_negatives(sort_func):
    """Test sorting lists containing duplicate values and negative numbers."""
    arr = [3, -1, 3, 0, -5, 2]
    expected = [-5, -1, 0, 2, 3, 3]
    res = sort_func(arr.copy())
    assert res["sorted_list"] == expected


@pytest.mark.parametrize("sort_func", [bubble_sort, insertion_sort])
def test_strings(sort_func):
    """Test sorting lists of strings alphabetically."""
    arr = ["cherry", "banana", "apple", "date"]
    expected = ["apple", "banana", "cherry", "date"]
    res = sort_func(arr.copy())
    assert res["sorted_list"] == expected
