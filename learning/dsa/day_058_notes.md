# Day 058: Backtracking - N-Queens & Permutations

## Overview
Implement classical backtracking algorithms to solve the N-Queens puzzle and generate sequence permutations (including duplicate-handling permutation filtering).

## Objectives
- Understand algorithmic mechanics of Backtracking: N-Queens & Permutations.
- Implement unit tests for edge cases.

## Key Concepts
Backtracking is an algorithmic technique for solving optimization and search problems incrementally by trying options and abandoning ('backtracking') choices that fail to satisfy constraints.

### 1. N-Queens Problem
- **Constraints**: No two queens can share the same row, column, positive diagonal (`row + col`), or negative diagonal (`row - col`).
- **State Tracking**: Using sets (`cols`, `pos_diag`, `neg_diag`) allows O(1) checks before placing a queen on row `r` and column `c`.
- **Bitmask Optimization**: Counting total solutions can be sped up significantly by using bitwise operations where integer bit representations mark occupied columns and diagonals.

### 2. Permutations & Duplicate Pruning
- **Standard Permutations**: Tracks visited elements using a boolean `used` array.
- **Handling Duplicates (`permute_unique`)**: Sorting the input array enables duplicate pruning. If `nums[i] == nums[i-1]` and `nums[i-1]` has not been used in the current branch, processing `nums[i]` would create duplicate search subtrees and is pruned.
