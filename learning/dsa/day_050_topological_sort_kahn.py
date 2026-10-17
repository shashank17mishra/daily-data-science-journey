"""
Day 50: Topological Sort using Kahn's Algorithm (BFS-based).

Topological sorting for a Directed Acyclic Graph (DAG) is a linear ordering of vertices
such that for every directed edge u -> v, vertex u comes before v in the ordering.
Kahn's algorithm repeatedly removes nodes with in-degree 0 and updates neighbor degrees.
"""

from collections import deque
from typing import Dict, List, TypeVar

T = TypeVar("T")


class CycleDetectedError(ValueError):
    """Exception raised when a cycle is detected in the directed graph."""

    pass


def topological_sort_kahn(graph: Dict[T, List[T]]) -> List[T]:
    """Perform topological sort on a graph represented as an adjacency dictionary.

    Args:
        graph: Dictionary mapping node -> list of destination nodes (outgoing edges).

    Returns:
        List of nodes in topologically sorted order.

    Raises:
        CycleDetectedError: If the graph contains at least one directed cycle.
    """
    in_degree: Dict[T, int] = {}

    # Initialize in-degree count for all reachable or declared nodes
    for u in graph:
        if u not in in_degree:
            in_degree[u] = 0
        for v in graph[u]:
            if v not in in_degree:
                in_degree[v] = 0

    # Calculate actual in-degrees
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    # Queue of all nodes with 0 in-degree
    zero_in_degree_queue: deque[T] = deque(
        [node for node, degree in in_degree.items() if degree == 0]
    )

    topological_order: List[T] = []

    while zero_in_degree_queue:
        node = zero_in_degree_queue.popleft()
        topological_order.append(node)

        # Process outgoing edges
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree_queue.append(neighbor)

    # If processed nodes count does not match total nodes, graph has a cycle
    if len(topological_order) != len(in_degree):
        raise CycleDetectedError(
            "Graph contains at least one directed cycle; topological order impossible."
        )

    return topological_order


def topological_sort_from_edges(
    num_nodes: int, edges: List[tuple[int, int]]
) -> List[int]:
    """Perform topological sort given node count and edge list (0-indexed nodes).

    Args:
        num_nodes: Total number of nodes (labeled 0 to num_nodes - 1).
        edges: List of (source, target) directed edges.

    Returns:
        List of node indices in topological order.

    Raises:
        ValueError: If an edge references an out-of-bounds node index.
        CycleDetectedError: If graph contains a cycle.
    """
    graph: Dict[int, List[int]] = {i: [] for i in range(num_nodes)}
    for src, dst in edges:
        if not (0 <= src < num_nodes) or not (0 <= dst < num_nodes):
            raise ValueError(
                f"Edge ({src}, {dst}) contains out-of-bounds node index for num_nodes={num_nodes}."
            )
        graph[src].append(dst)

    return topological_sort_kahn(graph)
