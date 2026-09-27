# Day 031: Big-O Time & Space Complexity

## Overview
Implementation and programmatic trade-off analysis of Big-O time and space complexity profiles (O(N^2)/O(1), O(N log N)/O(N), and O(N)/O(N)) using the Two-Sum problem and custom operation counter instrumentation.

## Objectives
- Understand algorithmic mechanics of Big-O Time & Space Complexity.
- Implement unit tests for edge cases.

## Key Concepts
This exercise illustrates Big-O Time and Space Complexity trade-offs programmatically:
1. **Brute Force**: Iterates through all pairs yielding O(N^2) time complexity and O(1) auxiliary space.
2. **Sorting + Two Pointers**: Pairs elements with original indices and sorts them in O(N log N) time, followed by a linear scan O(N) using two pointers. Auxiliary space is O(N) due to tuple allocations.
3. **Hash Map**: Uses single-pass lookup with O(1) average hash access, achieving O(N) time complexity at the cost of O(N) auxiliary space.
4. **OperationCounter**: Instrumenting step counts programmatically demonstrates how execution operations scale relative to input size N, reinforcing theoretical complexity guarantees.
