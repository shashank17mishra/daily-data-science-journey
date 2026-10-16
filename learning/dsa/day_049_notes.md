# Day 049: Dijkstra's Shortest Path Algorithm

## Overview
Implementation of Dijkstra's Shortest Path Algorithm using a priority queue (min-heap) for single-source shortest path calculation on weighted graphs with non-negative edge weights.

## Objectives
- Understand algorithmic mechanics of Dijkstra's Shortest Path Algorithm.
- Implement a priority-queue-backed shortest path calculation in Python.
- Reconstruct the shortest path from single-source distances and predecessors.
- Implement unit tests for edge cases including unreachable nodes, self-loops, single nodes, and negative weight detection.

## Key Concepts
Dijkstra's algorithm is a greedy algorithm that computes single-source shortest paths in weighted graphs with non-negative edge weights.

Key Concepts Implemented:
1. **Priority Queue Optimization**: Uses Python's standard `heapq` module to quickly retrieve the non-visited node with the minimum distance. Time complexity per extraction is O(log V).
2. **Relaxation Step**: For each neighbor, checks if `distances[current] + weight < distances[neighbor]`. If so, updates the shortest distance and tracks the predecessor node for path reconstruction.
3. **Stale Node Rejection**: If `current_dist > distances[current_node]`, skips processing to account for duplicate node insertions into the priority queue.
4. **Path Reconstruction**: Backtracks from the destination target to the start node using the `predecessors` map and reverses the resulting list.

Time & Space Complexity:
- Time Complexity: O((V + E) log V) where V is the number of vertices and E is the number of edges.
- Auxiliary Space Complexity: O(V + E) for storing graph structures, distances, and priority queue items.
