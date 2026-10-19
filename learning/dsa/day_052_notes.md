# Day 052: DP 0/1 Knapsack Problem

## Overview
Implementation of the 0/1 Knapsack Problem using top-down recursion with memoization, 2D bottom-up dynamic programming with path reconstruction, and 1D space-optimized dynamic programming.

## Objectives
- Understand algorithmic mechanics of DP: 0/1 Knapsack Problem.
- Implement unit tests for edge cases.

## Key Concepts
The 0/1 Knapsack problem is a foundational dynamic programming challenge where each item can either be included (1) or excluded (0). 

1. Top-Down Recursion with Memoization: Recursively decides whether to include or skip the item at `index`, caching results using state tuple `(index, remaining_capacity)` to reduce time complexity from $O(2^n)$ to $O(n \times W)$.
2. 2D Bottom-Up DP: Constructs a dynamic programming matrix `dp[i][c]` representing the max value achievable using a subset of the first `i` items and capacity `c`. Path reconstruction backtracks from `dp[n][capacity]` to find which specific item indices were included.
3. 1D Space Optimization: Observes that state transitions only depend on the previous item row (`i-1`). Iterating capacity backwards from `capacity` down to `weight` allows updating the DP state in-place using a single 1D array of size $W+1$, reducing space complexity from $O(n \times W)$ to $O(W)$.
