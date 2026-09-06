from learning.dsa.day_009_sorting import merge_sort

def test_merge_sort_basic():
    arr = [38, 27, 43, 3, 9, 82, 10]
    assert merge_sort(arr) == [3, 9, 10, 27, 38, 43, 82]

def test_merge_sort_empty_and_single():
    assert merge_sort([]) == []
    assert merge_sort([42]) == [42]

def test_merge_sort_duplicates():
    arr = [5, 1, 5, 2, 1]
    assert merge_sort(arr) == [1, 1, 2, 5, 5]
