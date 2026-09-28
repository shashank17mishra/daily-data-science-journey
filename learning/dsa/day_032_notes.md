# Day 032: Arrays & Dynamic Matrix Operations

## Overview
Implementation of a dynamic 2D numerical matrix class featuring dynamic resizing, rotational/transposition operations, and O(1) 2D range sum queries using cached prefix sums.

## Objectives
- Understand algorithmic mechanics of Arrays & Dynamic Matrix Operations.
- Implement unit tests for edge cases.

## Key Concepts
This exercise covers the core algorithms involved in 2D array and matrix manipulations:

1. Dynamic Resizing: Rows and columns can expand or shrink dynamically. When expanding, fill values pad the array; when shrinking, slices truncate existing data.
2. In-Place Transposition & Rotation: Transpositions swap row and column dimensions. Rotating 90 degrees clockwise is achieved via transpose followed by row reversal; counter-clockwise rotation reverses rows followed by transpose.
3. 2D Prefix Sum (Range Sum Query 2D): Precomputing a 2D prefix sum array allows submatrix sum queries for any subgrid [r1..r2, c1..c2] in O(1) time using the inclusion-exclusion principle: sum = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]. Cache invalidation ensures accuracy whenever elements or matrix structures change.
