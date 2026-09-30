# Day 034: Sliding Window Pattern

## Overview
Implementation of fixed-size and dynamic-size sliding window algorithms to solve fundamental array and string problems efficiently in linear time O(N).

## Objectives
- Understand algorithmic mechanics of Sliding Window Pattern.
- Implement unit tests for edge cases.

## Key Concepts
The Sliding Window pattern reduces brute-force nested loop complexities from O(N^2) or O(N^3) to linear O(N) time complexity by maintaining a dynamic or fixed sub-segment of data as two pointers move through a contiguous collection.

Key variations included in this module:
1. Fixed-size Window (`max_subarray_sum_fixed`): Maintains a window of exact size `k`. When shifting right, the outgoing element (`arr[i-k]`) is subtracted and incoming element (`arr[i]`) is added.
2. Dynamic Window Expansion/Contraction (`min_subarray_len_target`): Expands the right pointer to satisfy a condition (sum >= target), then contracts the left pointer to find the optimal minimum length.
3. Auxiliary Frequency Map (`longest_substring_k_distinct`): Uses a hash map to track item frequencies within the window, dynamically shrinking from the left when the number of distinct items exceeds `k`.
