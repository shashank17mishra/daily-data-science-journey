# Day 039: Quick Sort & Partitioning

## Overview
An in-depth implementation of the Quick Sort algorithm featuring both Lomuto and Hoare partitioning schemes. This exercise highlights the mechanics of in-place partitioning, pivot selection, and recursion control, backed by a comprehensive pytest suite covering edge cases.

## Objectives
- Understand algorithmic mechanics of Quick Sort & Partitioning.
- Implement and compare Lomuto and Hoare partitioning schemes.
- Implement unit tests for edge cases including empty arrays, duplicates, and pre-sorted arrays.

## Key Concepts
Quick Sort is a highly efficient, divide-and-conquer sorting algorithm. On average, it achieves O(N log N) time complexity. The core of Quick Sort lies in its partitioning scheme:

1. **Lomuto Partitioning**: This scheme is easier to implement and understand. It typically chooses the last element as the pivot. It maintains an index `i` representing the boundary of elements smaller than or equal to the pivot. It scans the array with a pointer `j`, swapping elements smaller than the pivot into the `i` region. Finally, the pivot is swapped into its correct place.

2. **Hoare Partitioning**: This scheme uses two pointers starting at the extreme ends of the array. They move toward each other until they detect an inversion (an element on the left larger than the pivot, and an element on the right smaller than the pivot), at which point they swap them. Hoare's scheme is generally more efficient than Lomuto's because it performs three times fewer swaps on average and handles duplicates efficiently.
