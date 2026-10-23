# Day 056: Union-Find (Disjoint Set)

## Overview
Implementation of an advanced Disjoint-Set (Union-Find) data structure supporting generic hashable elements, path compression, union by rank, dynamic addition, component tracking, and comprehensive unit tests.

## Objectives
- Understand algorithmic mechanics of Union-Find (Disjoint Set).
- Implement unit tests for edge cases.

## Key Concepts
The Union-Find (Disjoint-Set) data structure tracks partitionings of a set into disjoint components. It supports two primary operations: `find`, which identifies the representative of a set containing an element, and `union`, which merges two sets.

Two core optimizations achieve near-constant time complexity:
1. Path Compression: Flattens the structure of the tree whenever `find` is called, pointing all traversed elements directly to the root.
2. Union by Rank: Always attaches the smaller tree under the root of the larger tree to keep tree heights minimal.

With both optimizations, operations run in nearly $O(\alpha(N))$ amortized time, where $\alpha$ is the Inverse Ackermann Function.
