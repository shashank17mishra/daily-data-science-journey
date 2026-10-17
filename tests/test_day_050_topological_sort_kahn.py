"""
Unit tests for Kahn's Algorithm for Topological Sort.
"""

import pytest
from learning.dsa.day_050_topological_sort_kahn import (
    CycleDetectedError,
    topological_sort_from_edges,
    topological_sort_kahn,
)


def is_valid_topological_order(graph: dict, order: list) -> bool:
    """Helper function to verify if an ordering satisfies directed edge constraints."""
    node_to_position = {node: i for i, node in enumerate(order)}
    if len(node_to_position) != len(order):
        return False  # Duplicate entries in order

    for u in graph:
        for v in graph[u]:
            if u not in node_to_position or v not in node_to_position:
                return False
            if node_to_position[u] >= node_to_position[v]:
                return False
    return True


def test_simple_dag():
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }
    order = topological_sort_kahn(graph)
    assert len(order) == 4
    assert is_valid_topological_order(graph, order)


def test_complex_dag():
    graph = {
        5: [11],
        7: [11, 8],
        3: [8, 10],
        11: [2, 9, 10],
        8: [9],
        2: [],
        9: [],
        10: [],
    }
    order = topological_sort_kahn(graph)
    assert len(order) == 8
    assert is_valid_topological_order(graph, order)


def test_single_node():
    graph = {"A": []}
    order = topological_sort_kahn(graph)
    assert order == ["A"]


def test_empty_graph():
    graph = {}
    order = topological_sort_kahn(graph)
    assert order == []


def test_disconnected_dag():
    graph = {
        1: [2],
        2: [],
        3: [4],
        4: [],
    }
    order = topological_sort_kahn(graph)
    assert len(order) == 4
    assert is_valid_topological_order(graph, order)


def test_cycle_detection_simple():
    graph = {
        "A": ["B"],
        "B": ["A"],
    }
    with pytest.raises(CycleDetectedError):
        topological_sort_kahn(graph)


def test_self_loop():
    graph = {
        "A": ["A"],
    }
    with pytest.raises(CycleDetectedError):
        topological_sort_kahn(graph)


def test_cycle_in_subgraph():
    graph = {
        "Start": ["A"],
        "A": ["B"],
        "B": ["C"],
        "C": ["A"],
    }
    with pytest.raises(CycleDetectedError):
        topological_sort_kahn(graph)


def test_edges_api():
    num_nodes = 6
    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    order = topological_sort_from_edges(num_nodes, edges)

    graph = {i: [] for i in range(num_nodes)}
    for u, v in edges:
        graph[u].append(v)

    assert len(order) == num_nodes
    assert is_valid_topological_order(graph, order)


def test_edges_api_invalid_node_index():
    num_nodes = 3
    edges = [(0, 1), (1, 5)]
    with pytest.raises(ValueError, match="out-of-bounds"):
        topological_sort_from_edges(num_nodes, edges)
