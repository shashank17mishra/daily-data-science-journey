# Day 036: Binary Search & Rotated Array Search

## Overview
Implementation of standard binary search, searching in a rotated sorted array, and finding the minimum element in a rotated sorted array in logarithmic time O(log n).

## Objectives
- Understand algorithmic mechanics of Binary Search & Rotated Array Search.
- Implement unit tests for edge cases.

## Key Concepts
Binary search operates in O(log n) time complexity by repeatedly dividing the search interval in half. When searching in a rotated sorted array, the key invariant is that dividing the array at any index mid results in at least one contiguous sorted half (either left or right). By comparing the target value against the bounds of the sorted half, we can determine whether target lies within that half or if search should proceed in the other half. Finding the minimum element uses a related property: comparing `nums[mid]` with `nums[right]` reveals whether the inflection/pivot point (the minimum element) lies to the right of `mid` (when `nums[mid] > nums[right]`) or at/to the left of `mid` (when `nums[mid] <= nums[right]`).
