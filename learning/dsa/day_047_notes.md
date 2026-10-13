# Day 047: Graph BFS Traversal

## Overview
This exercise focuses on implementing the Breadth-First Search (BFS) algorithm for graph traversal. BFS is a fundamental graph algorithm used to explore all reachable nodes in a graph layer by layer, starting from a given source node. It's commonly used for finding the shortest path in unweighted graphs, network broadcasting, and web crawling. The implementation will use an adjacency list representation for the graph and a queue data structure to manage nodes to visit.

## Objectives
- Understand the algorithmic mechanics of Graph BFS Traversal.
- Implement a robust BFS traversal function using an adjacency list and a queue.
- Develop comprehensive unit tests for various graph structures and edge cases, including disconnected graphs, cycles, and invalid start nodes.

## Key Concepts
The Breadth-First Search (BFS) algorithm explores a graph level by level. It starts at a source node, visits all its immediate neighbors, then all their unvisited neighbors, and so on. This "layer by layer" exploration ensures that all nodes at a given distance 'k' from the source are visited before any nodes at distance 'k+1'.

Key components of the BFS implementation:
1.  **Adjacency List:** The graph is represented as a dictionary where each key is a node, and its value is a list of its direct neighbors. This allows for efficient lookup of neighbors.
2.  **Queue:** A `collections.deque` is used as a queue. Nodes are added to the right (enqueue) and removed from the left (dequeue). This FIFO (First-In, First-Out) behavior is crucial for BFS's level-by-level exploration.
3.  **Visited Set:** A `set` is used to keep track of nodes that have already been added to the queue or processed. This prevents revisiting nodes, avoids infinite loops in graphs with cycles, and ensures each node is processed exactly once.

The `bfs_traversal` function initializes the `visited` set and the `queue` with the `start_node`. It then iteratively dequeues a node, adds it to the `traversal_order`, and enqueues all its unvisited neighbors. The process continues until the queue is empty, at which point all reachable nodes have been visited. Edge cases like an empty graph or a start node not present in the graph are handled by returning an empty list.
