# Day 050: Topological Sort (Kahn's Algorithm)

## Overview
Implementation of Topological Sorting for Directed Acyclic Graphs (DAG) using Kahn's Algorithm (BFS-based in-degree processing) with cycle detection.

## Objectives
- Understand algorithmic mechanics of Topological Sort (Kahn's Algorithm).
- Implement unit tests for edge cases.

## Key Concepts
Kahn's Algorithm is a Breadth-First Search (BFS) method for finding a topological ordering of vertices in a Directed Acyclic Graph (DAG).

### Key Concepts:
1. **In-Degree Calculation**: Compute the number of incoming edges for every node.
2. **Zero In-Degree Queue**: Enqueue all vertices with an initial in-degree of 0 (nodes with no dependencies).
3. **Iterative Processing**: Pop a node from the queue, place it in the output ordering, and decrement the in-degree of all its target neighbors.
4. **Dependency Resolution**: Whenever a neighbor's in-degree reaches 0, enqueue it.
5. **Cycle Detection**: If the number of nodes in the output order is less than the total node count, at least one directed cycle exists because cyclic nodes never reach an in-degree of 0.

### Complexity:
- **Time Complexity**: O(V + E) where V is total vertices and E is total edges.
- **Space Complexity**: O(V) for the queue and in-degree mapping storage.
