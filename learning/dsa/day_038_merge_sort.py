"""Merge Sort implementation using the Divide and Conquer paradigm."""

from typing import Any, Callable, List, Optional, Tuple, TypeVar

T = TypeVar("T")


def merge_sort(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
) -> List[T]:
    """Sort a list using the Merge Sort algorithm.

    Divide and Conquer Strategy:
    1. Divide: Split array into two halves at mid index.
    2. Conquer: Recursively sort left and right halves.
    3. Combine: Merge the two sorted halves into a single sorted list.

    Args:
        arr: Input list to be sorted.
        key: Single argument function used to extract comparison key.
        reverse: If True, sort in descending order.

    Returns:
        A new list containing elements in sorted order.
    """
    if len(arr) <= 1:
        return list(arr)

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key=key, reverse=reverse)
    right = merge_sort(arr[mid:], key=key, reverse=reverse)

    return _merge(left, right, key=key, reverse=reverse)


def _merge(
    left: List[T],
    right: List[T],
    key: Optional[Callable[[T], Any]],
    reverse: bool,
) -> List[T]:
    """Merge two sorted lists preserving stability."""
    merged: List[T] = []
    i = j = 0

    key_fn = key if key is not None else lambda x: x

    while i < len(left) and j < len(right):
        left_key = key_fn(left[i])
        right_key = key_fn(right[j])

        if (left_key <= right_key) if not reverse else (left_key >= right_key):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def count_inversions(arr: List[int]) -> Tuple[List[int], int]:
    """Count inversions in an array using modified Merge Sort.

    An inversion occurs when i < j and arr[i] > arr[j].
    Time Complexity: O(N log N)
    Space Complexity: O(N)

    Args:
        arr: List of integers.

    Returns:
        Tuple containing (sorted_list, total_inversion_count).
    """
    if len(arr) <= 1:
        return list(arr), 0

    mid = len(arr) // 2
    left_sorted, left_inv = count_inversions(arr[:mid])
    right_sorted, right_inv = count_inversions(arr[mid:])

    merged_sorted, split_inv = _merge_and_count(left_sorted, right_sorted)
    return merged_sorted, left_inv + right_inv + split_inv


def _merge_and_count(left: List[int], right: List[int]) -> Tuple[List[int], int]:
    """Merge two sorted sublists and count split inversions."""
    merged: List[int] = []
    i = j = 0
    inversions = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            inversions += len(left) - i

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inversions
