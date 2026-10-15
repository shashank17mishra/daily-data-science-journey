import pytest
from learning.dsa.day_048_graph_dfs_traversal import dfs_traversal

def test_dfs_simple_path():
    """Test DFS on a simple linear graph."""
    graph = {
        'A': ['B'],
        'B': ['A', 'C'],
        'C': ['B', 'D'],
        'D': ['C']
    }
    assert dfs_traversal(graph, 'A') == ['A', 'B', 'C', 'D']
    assert dfs_traversal(graph, 'D') == ['D', 'C', 'B', 'A']

def test_dfs_branched_graph():
    """Test DFS on a graph with branching paths."""
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'E'],
        'D': ['B'],
        'E': ['C']
    }
    # The order depends on the adjacency list order. 'B' is listed before 'C' for 'A'.
    assert dfs_traversal(graph, 'A') == ['A', 'B', 'D', 'C', 'E']
    # Starting from 'C', 'A' is listed before 'E'
    assert dfs_traversal(graph, 'C') == ['C', 'A', 'B', 'D', 'E']

def test_dfs_with_cycle():
    """Test DFS on a graph containing a cycle, ensuring no infinite loop."""
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['B', 'C']
    }
    # Expected order from 'A': A -> B -> D -> C (C is visited last as D's neighbor)
    assert dfs_traversal(graph, 'A') == ['A', 'B', 'D', 'C']
    # Expected order from 'C': C -> A -> B -> D
    assert dfs_traversal(graph, 'C') == ['C', 'A', 'B', 'D']

def test_dfs_disconnected_graph():
    """Test DFS on a disconnected graph, starting in one component."""
    graph = {
        '1': ['2'],
        '2': ['1'],
        'A': ['B'],
        'B': ['A'],
        'X': [] # Isolated node
    }
    assert dfs_traversal(graph, '1') == ['1', '2']
    assert dfs_traversal(graph, 'A') == ['A', 'B']
    assert dfs_traversal(graph, 'X') == ['X'] # Isolated node is visited

def test_dfs_single_node_graph():
    """Test DFS on a graph with only a single node."""
    graph = {'A': []}
    assert dfs_traversal(graph, 'A') == ['A']

def test_dfs_empty_graph():
    """Test DFS on an empty graph."""
    graph = {}
    assert dfs_traversal(graph, 'A') == []

def test_dfs_start_node_not_in_graph():
    """Test DFS when the start node is not a key in the graph."""
    graph = {
        'A': ['B'],
        'B': ['A']
    }
    assert dfs_traversal(graph, 'Z') == []

def test_dfs_complex_graph():
    """Test DFS on a more complex graph structure."""
    graph = {
        '0': ['1', '2'],
        '1': ['0', '3', '4'],
        '2': ['0', '4'],
        '3': ['1', '5'],
        '4': ['1', '2', '5'],
        '5': ['3', '4']
    }
    # Expected order from '0': 0 -> 1 -> 3 -> 5 -> 4 -> 2
    assert dfs_traversal(graph, '0') == ['0', '1', '3', '5', '4', '2']
    # Expected order from '3': 3 -> 1 -> 0 -> 2 -> 4 -> 5
    assert dfs_traversal(graph, '3') == ['3', '1', '0', '2', '4', '5']

def test_dfs_graph_with_no_edges():
    """Test DFS on a graph where nodes exist but have no edges."""
    graph = {
        'A': [],
        'B': [],
        'C': []
    }
    assert dfs_traversal(graph, 'A') == ['A']
    assert dfs_traversal(graph, 'B') == ['B']
    assert dfs_traversal(graph, 'C') == ['C']
