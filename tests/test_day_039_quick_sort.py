import pytest
import random
from learning.dsa.day_039_quick_sort import quick_sort, lomuto_partition, hoare_partition

@pytest.mark.parametrize("scheme", ["lomuto", "hoare"])
def test_empty_and_single_element(scheme):
    assert quick_sort([], scheme=scheme) == []
    assert quick_sort([42], scheme=scheme) == [42]

@pytest.mark.parametrize("scheme", ["lomuto", "hoare"])
def test_already_sorted(scheme):
    arr = [1, 2, 3, 4, 5, 6, 7]
    assert quick_sort(arr.copy(), scheme=scheme) == [1, 2, 3, 4, 5, 6, 7]

@pytest.mark.parametrize("scheme", ["lomuto", "hoare"])
def test_reverse_sorted(scheme):
    arr = [7, 6, 5, 4, 3, 2, 1]
    assert quick_sort(arr.copy(), scheme=scheme) == [1, 2, 3, 4, 5, 6, 7]

@pytest.mark.parametrize("scheme", ["lomuto", "hoare"])
def test_duplicates(scheme):
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    expected = sorted(arr)
    assert quick_sort(arr.copy(), scheme=scheme) == expected

@pytest.mark.parametrize("scheme", ["lomuto", "hoare"])
def test_random_arrays(scheme):
    random.seed(42)
    for _ in range(10):
        arr = [random.randint(-100, 100) for _ in range(50)]
        expected = sorted(arr)
        assert quick_sort(arr.copy(), scheme=scheme) == expected

def test_invalid_scheme():
    with pytest.raises(ValueError):
        quick_sort([3, 1, 2], scheme="invalid_scheme")

def test_lomuto_partition_mechanics():
    # Pivot is last element (5)
    arr = [4, 1, 7, 3, 5]
    p = lomuto_partition(arr, 0, len(arr) - 1)
    # Elements before p should be <= pivot (5)
    # Elements after p should be > pivot (5)
    assert all(x <= 5 for x in arr[:p])
    assert arr[p] == 5
    assert all(x > 5 for x in arr[p+1:])

def test_hoare_partition_mechanics():
    # Pivot is first element (5)
    arr = [5, 3, 8, 4, 2, 7, 1, 10]
    p = hoare_partition(arr, 0, len(arr) - 1)
    # Hoare partition guarantees elements in arr[low..p] <= elements in arr[p+1..high]
    assert max(arr[:p+1]) <= min(arr[p+1:])
