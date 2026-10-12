# Day 046: Heaps & Priority Queues

## Overview
An advanced implementation of an Indexed Priority Queue (Indexed Min-Heap) supporting O(log N) key updates, arbitrary item deletions, and O(1) key lookup and containment checks.

## Objectives
- Understand algorithmic mechanics of Heaps & Priority Queues.
- Implement unit tests for edge cases.

## Key Concepts
### Algorithmic Mechanics: Indexed Min-Heap

Standard binary heaps built on Python's `heapq` module do not support efficient priority updates or arbitrary key deletions. Finding an arbitrary item in standard binary heaps requires $O(N)$ linear scans.

An **Indexed Priority Queue (Indexed Min-Heap)** solves this by maintaining two synchronized data structures:
1. **Array/List (`_heap`)**: Holds standard binary heap nodes `(key, priority)` arranged as a complete binary tree.
2. **Position Hash Map (`_position_map`)**: Maps each unique `key` to its exact array index in `_heap`.

#### Key Operations & Time Complexities:
- **`push(key, priority)`**: Appends the node to `_heap`, stores position in `_position_map`, and calls `_sift_up` ($O(\log N)$).
- **`pop()`**: Replaces the root with the last element, deletes root from `_position_map`, and calls `_sift_down` ($O(\log N)$).
- **`update_priority(key, new_priority)`**: Looks up key index in $O(1)$, updates priority, and executes `_sift_up` if priority decreased or `_sift_down` if priority increased ($O(\log N)$).
- **`delete(key)`**: Locates key index in $O(1)$, swaps with the last element, pops the end, and balances the structure ($O(\log N)$).
- **`contains(key)` / `get_priority(key)`**: $O(1)$ direct dictionary operations.

This data structure is foundational in graph algorithms such as **Dijkstra's Shortest Path Algorithm** and **Prim's Minimum Spanning Tree Algorithm**.
