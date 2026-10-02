"""Binary Search and Rotated Array Algorithms.

This module provides implementations for standard binary search and variations
such as searching in a rotated sorted array and finding the minimum element
in a rotated sorted array.
"""

from typing import List


def binary_search(arr: List[int], target: int) -> int:
    """Perform standard binary search on a sorted list of integers.

    Args:
        arr: A list of integers sorted in ascending order.
        target: The integer to search for.

    Returns:
        The 0-based index of target if found; otherwise -1.
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
    return -1


def search_rotated_array(nums: List[int], target: int) -> int:
    """Search for a target value in a rotated sorted array of distinct integers.

    Args:
        nums: A list of distinct integers sorted in ascending order then rotated.
        target: The integer to search for.

    Returns:
        The 0-based index of target if present; otherwise -1.
    """
    if not nums:
        return -1

    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid

        # Check if the left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Otherwise, the right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


def find_min_rotated_array(nums: List[int]) -> int:
    """Find the minimum value in a rotated sorted array of distinct integers.

    Args:
        nums: A list of distinct integers sorted in ascending order then rotated.

    Returns:
        The minimum integer in the array.

    Raises:
        ValueError: If nums is empty.
    """
    if not nums:
        raise ValueError("Cannot find minimum in an empty array.")

    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return nums[left]
