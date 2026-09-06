from learning.dsa.day_008_binary_search import binary_search

def test_binary_search_found():
    arr = [1, 3, 5, 7, 9, 11, 13]
    assert binary_search(arr, 7) == 3
    assert binary_search(arr, 1) == 0
    assert binary_search(arr, 13) == 6

def test_binary_search_not_found():
    arr = [1, 3, 5, 7, 9, 11, 13]
    assert binary_search(arr, 4) is None
    assert binary_search(arr, 0) is None
    assert binary_search(arr, 20) is None
