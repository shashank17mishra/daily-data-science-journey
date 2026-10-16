"""
Dijkstra's Shortest Path Algorithm Implementation.

This module provides a class representation of a weighted graph and implements
Dijkstra's algorithm using a min-heap priority queue to find the shortest path
between nodes in graphs with non-negative edge weights.
"""

import heapq
from typing import Dict, List, Optional, Tuple


class WeightedGraph:
    """Represents a weighted directed or undirected graph using adjacency lists."""

    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = {}

    def add_node(self, node: str) -> None:
        """Add a node to the graph if it doesn't already exist."""
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, u: str, v: str, weight: float) -> None:
        """
        Add a weighted edge between nodes u and v.

        Args:
            u: Source node name.
            v: Destination node name.
            weight: Non-negative weight/cost of the edge.

        Raises:
            ValueError: If weight is negative.
        """
        if weight < 0:
            raise ValueError(f"Edge weight cannot be negative: {weight}")

        self.add_node(u)
        self.add_node(v)

        self.adjacency_list[u].append((v, float(weight)))
        if not self.directed:
            self.adjacency_list[v].append((u, float(weight)))

    def dijkstra(self, start_node: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
        """
        Computes the shortest paths from start_node to all reachable nodes using Dijkstra's algorithm.

        Args:
            start_node: Starting node identifier.

        Returns:
            Tuple containing:
                - distances: Dictionary mapping each node to its shortest distance from start_node.
                - predecessors: Dictionary mapping each node to its predecessor on the shortest path.

        Raises:
            KeyError: If start_node is not present in the graph.
        """
        if start_node not in self.adjacency_list:
            raise KeyError(f"Start node '{start_node}' does not exist in the graph.")

        distances: Dict[str, float] = {node: float("inf") for node in self.adjacency_list}
        predecessors: Dict[str, Optional[str]] = {node: None for node in self.adjacency_list}
        distances[start_node] = 0.0

        # Min-heap priority queue stores tuples of (distance, node)
        priority_queue: List[Tuple[float, str]] = [(0.0, start_node)]

        while priority_queue:
            current_dist, current_node = heapq.heappop(priority_queue)

            # Skip stale entries from the priority queue
            if current_dist > distances[current_node]:
                continue

            for neighbor, weight in self.adjacency_list[current_node]:
                distance = current_dist + weight

                # Relaxation step
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, predecessors

    def get_shortest_path(self, start_node: str, target_node: str) -> Tuple[List[str], float]:
        """
        Reconstructs the shortest path and computes total distance between start_node and target_node.

        Args:
            start_node: Starting node identifier.
            target_node: Destination node identifier.

        Returns:
            Tuple containing:
                - path: List of node names representing the sequence of nodes in the shortest path.
                - total_distance: Sum of edge weights along the shortest path.
        """
        if target_node not in self.adjacency_list:
            raise KeyError(f"Target node '{target_node}' does not exist in the graph.")

        distances, predecessors = self.dijkstra(start_node)

        if distances[target_node] == float("inf"):
            return [], float("inf")

        path = []
        curr: Optional[str] = target_node
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]

        path.reverse()
        return path, distances[target_node]
