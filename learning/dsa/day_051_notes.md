# Day 051: Dynamic Programming - 1D DP Algorithms

## Overview
Implementation of advanced 1D Dynamic Programming algorithms, including wildcard string decoding, maximum subarray sum partitioning, and multi-interval cost optimization.

## Objectives
- Understand algorithmic mechanics of Dynamic Programming: 1D DP.
- Implement unit tests for edge cases.

## Key Concepts
This exercise covers three core 1D Dynamic Programming problems with varying subproblem transition mechanics:

1. **Decode Ways II (Wildcards)**: State transitions depend on current and previous characters. By tracking $DP[i-1]$ and $DP[i-2]$, we compute total combinations in $O(N)$ time and $O(1)$ extra space.
2. **Partition Array for Maximum Sum**: Demonstrates optimal partitioning where state $DP[i]$ looks back up to $k$ steps to find the optimal subarray extension.
3. **Minimum Travel Cost**: Represents day-by-day decision making where each state evaluates 1-day, 7-day, and 30-day ticket options.
