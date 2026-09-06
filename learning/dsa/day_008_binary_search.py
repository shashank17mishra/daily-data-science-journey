"""
Day 008: Data Structures & Algorithms - Binary Search Implementation.
"""
from typing import List, Optional

def binary_search(arr: List[int], target: int) -> Optional[int]:
    """
    Performs binary search on a sorted array of integers.
    Returns the index of target if found, else None.
    Time Complexity: O(log n), Space Complexity: O(1).
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None
