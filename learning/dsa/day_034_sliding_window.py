"""Sliding Window Pattern Implementations.

This module provides standard implementations of the Sliding Window technique:
1. Fixed-size sliding window (Maximum sum subarray of size k).
2. Variable-size sliding window with target sum (Minimum length subarray with sum >= target).
3. Variable-size sliding window with hash map (Longest substring with at most k distinct characters).
"""

from typing import List


def max_subarray_sum_fixed(arr: List[int], k: int) -> int:
    """Find the maximum sum of a contiguous subarray of fixed size k.

    Args:
        arr: List of integers.
        k: Size of the sliding window.

    Returns:
        Maximum sum of any contiguous subarray of length k.

    Raises:
        ValueError: If k is non-positive or greater than array length.
    """
    if k <= 0:
        raise ValueError("Window size k must be positive.")
    if k > len(arr):
        raise ValueError("Window size k cannot exceed array length.")

    window_sum = sum(arr[:k])
    max_sum = window_sum

    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        if window_sum > max_sum:
            max_sum = window_sum

    return max_sum


def min_subarray_len_target(target: int, arr: List[int]) -> int:
    """Find the minimal length of a contiguous subarray whose sum is >= target.

    Args:
        target: Positive target sum.
        arr: List of positive integers.

    Returns:
        Minimal length of a matching contiguous subarray, or 0 if none found.

    Raises:
        ValueError: If target is non-positive.
    """
    if target <= 0:
        raise ValueError("Target must be positive.")

    left = 0
    current_sum = 0
    min_len = float("inf")

    for right in range(len(arr)):
        current_sum += arr[right]

        while current_sum >= target:
            min_len = min(min_len, right - left + 1)
            current_sum -= arr[left]
            left += 1

    return int(min_len) if min_len != float("inf") else 0


def longest_substring_k_distinct(s: str, k: int) -> int:
    """Find the length of the longest substring containing at most k distinct characters.

    Args:
        s: Input string.
        k: Maximum number of distinct characters allowed.

    Returns:
        Length of the longest valid substring.
    """
    if k <= 0 or not s:
        return 0

    left = 0
    max_len = 0
    char_freq = {}

    for right in range(len(s)):
        char = s[right]
        char_freq[char] = char_freq.get(char, 0) + 1

        while len(char_freq) > k:
            left_char = s[left]
            char_freq[left_char] -= 1
            if char_freq[left_char] == 0:
                del char_freq[left_char]
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len
