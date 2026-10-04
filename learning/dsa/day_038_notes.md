# Day 038: Merge Sort (Divide & Conquer)

## Overview
Implementation of Merge Sort using top-down Divide and Conquer algorithm along with stability support, custom key functions, reverse ordering, and an application function for counting array inversions in O(N log N) time.

## Objectives
- Understand algorithmic mechanics of Merge Sort (Divide & Conquer).
- Implement unit tests for edge cases.

## Key Concepts
Merge Sort is a classic Divide and Conquer algorithm that operates in three steps: Divide the array into two halves, recursively Conquer by sorting both sub-arrays, and Combine the sorted sub-arrays in O(N) time using two pointers. Its worst-case and average-case time complexities are both O(N log N). Merge Sort is stable, preserving the original relative order of equal elements. Additionally, the standard merge step can be adapted to count inversions (pairs where i < j and arr[i] > arr[j]) in O(N log N) time by adding `len(left) - i` to the count whenever an element from the right sub-array is selected before an element in the left sub-array.
