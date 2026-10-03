# Day 037: Bubble & Insertion Sort

## Overview
An intermediate-level implementation of Bubble Sort and Insertion Sort. This implementation includes performance tracking (comparisons, swaps, and shifts) to demonstrate the algorithmic mechanics and efficiency differences between the two algorithms.

## Objectives
- Understand algorithmic mechanics of Bubble & Insertion Sort.
- Implement unit tests for edge cases.

## Key Concepts
This exercise implements two fundamental comparison-based sorting algorithms: Bubble Sort and Insertion Sort. 

1. **Bubble Sort**: Iteratively steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. It includes an early-exit optimization: if a full pass completes without any swaps, the list is already sorted, and the algorithm terminates early. This reduces the best-case time complexity to O(n).

2. **Insertion Sort**: Builds the final sorted array one item at a time. It is much more efficient in practice than bubble sort for small or nearly-sorted datasets. It has a best-case time complexity of O(n) when the array is already sorted.

Both implementations return metadata (comparisons, swaps/shifts) to help visualize and verify the inner mechanics of the algorithms under different scenarios (e.g., already sorted vs. reverse sorted).
