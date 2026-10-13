import pytest
from learning.dsa.day_047_graph_bfs_traversal import bfs_traversal

def test_bfs_simple_connected_graph():
    """Test BFS on a simple connected graph."""
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    expected_traversal = ['A', 'B', 'C', 'D', 'E', 'F']
    assert bfs_traversal(graph, 'A') == expected_traversal

def test_bfs_graph_with_cycle():
    """Test BFS on a graph containing a cycle."""
    graph = {
        0: [1, 2],
        1: [0, 3],
        2: [0, 4],
        3: [1, 5],
        4: [2, 5],
        5: [3, 4]
    }
    expected_traversal = [0, 1, 2, 3, 4, 5]
    assert bfs_traversal(graph, 0) == expected_traversal

def test_bfs_disconnected_graph():
    """Test BFS on a disconnected graph, starting from a node in one component."""
    graph = {
        'X': ['Y'],
        'Y': ['X'],
        'P': ['Q'],
        'Q': ['P']
    }
    assert bfs_traversal(graph, 'X') == ['X', 'Y']
    assert bfs_traversal(graph, 'P') == ['P', 'Q']

def test_bfs_single_node_graph():
    """Test BFS on a graph with only one node."""
    graph = {'A': []}
    assert bfs_traversal(graph, 'A') == ['A']

def test_bfs_empty_graph():
    """Test BFS on an empty graph."""
    graph = {}
    assert bfs_traversal(graph, 'A') == []

def test_bfs_start_node_not_in_graph():
    """Test BFS when the start node is not present in the graph."""
    graph = {'A': ['B'], 'B': []}
    assert bfs_traversal(graph, 'C') == []

def test_bfs_linear_graph():
    """Test BFS on a linear graph (like a linked list)."""
    graph = {
        1: [2],
        2: [3],
        3: [4],
        4: []
    }
    expected_traversal = [1, 2, 3, 4]
    assert bfs_traversal(graph, 1) == expected_traversal

def test_bfs_complex_graph_multiple_paths():
    """Test BFS on a more complex graph with multiple paths to nodes."""
    graph = {
        'S': ['A', 'B'],
        'A': ['C', 'D'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': ['F', 'G'],
        'E': ['G'],
        'F': [],
        'G': []
    }
    expected_traversal = ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
    assert bfs_traversal(graph, 'S') == expected_traversal

def test_bfs_no_neighbors():
    """Test BFS from a node with no neighbors."""
    graph = {
        'A': [],
        'B': ['C'],
        'C': []
    }
    assert bfs_traversal(graph, 'A') == ['A']
    assert bfs_traversal(graph, 'B') == ['B', 'C']
