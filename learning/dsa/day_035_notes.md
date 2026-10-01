# Day 035: Prefix Sum Arrays

## Overview
Implementation of 1D and 2D Prefix Sum Arrays (Summed-Area Table) to perform efficient range sum queries in O(1) time after O(N*M) preprocessing.

## Objectives
- Understand algorithmic mechanics of Prefix Sum Arrays.
- Implement unit tests for edge cases.

## Key Concepts
Prefix Sum is an algorithmic technique used to perform fast range sum queries on an array or matrix. By precomputing cumulative sums, we can answer any range query in O(1) time. For 1D arrays, the prefix sum at index `i` stores the sum of elements up to `i-1`. For 2D matrices, the Summed-Area Table stores the sum of the subgrid from (0,0) to (r,c). Range queries are resolved using the Inclusion-Exclusion Principle, subtracting overlapping regions to isolate the target subgrid sum.
