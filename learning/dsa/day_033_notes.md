# Day 033: Two Pointers Technique

## Overview
An implementation of classic Two Pointers algorithms: Two Sum II (Sorted Input) and Container With Most Water. These algorithms demonstrate how to optimize search space from O(N^2) to O(N) time complexity and O(1) auxiliary space by strategically moving pointers from both ends of an array.

## Objectives
- Understand algorithmic mechanics of Two Pointers Technique.
- Implement unit tests for edge cases.

## Key Concepts
The Two Pointers technique is a powerful algorithmic pattern used to solve array and string problems efficiently. By maintaining two indices (usually starting at opposite ends or moving at different speeds), we can prune the search space dynamically based on sorted properties or greedy choices. In `two_sum_sorted`, sorting allows us to increment the left pointer to increase the sum, or decrement the right pointer to decrease the sum. In `max_area`, we greedily move the pointer pointing to the shorter line because keeping the shorter line can never produce a larger area with a smaller width.
