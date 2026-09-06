"""
Day 009: Data Structures & Algorithms - Merge Sort (Divide & Conquer).
"""
from typing import List

def merge_sort(arr: List[int]) -> List[int]:
    """
    Performs recursive merge sort on a list of integers.
    Time Complexity: O(n log n), Space Complexity: O(n).
    """
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    left_sorted = merge_sort(arr[:mid])
    right_sorted = merge_sort(arr[mid:])

    return _merge(left_sorted, right_sorted)

def _merge(left: List[int], right: List[int]) -> List[int]:
    """Helper function to merge two sorted arrays."""
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
