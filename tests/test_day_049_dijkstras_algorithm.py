"""Unit tests for Dijkstra's Shortest Path Algorithm."""

import pytest
from learning.dsa.day_049_dijkstras_algorithm import WeightedGraph


@pytest.fixture
def sample_graph():
    """Fixture providing a standard directed weighted graph."""
    graph = WeightedGraph(directed=True)
    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("B", "C", 1)
    graph.add_edge("B", "D", 5)
    graph.add_edge("C", "D", 8)
    graph.add_edge("C", "E", 10)
    graph.add_edge("D", "E", 2)
    return graph


def test_dijkstra_shortest_distances(sample_graph):
    distances, predecessors = sample_graph.dijkstra("A")
    assert distances["A"] == 0
    assert distances["B"] == 4
    assert distances["C"] == 2
    assert distances["D"] == 9  # A -> B -> D is 4 + 5 = 9
    assert distances["E"] == 11  # A -> B -> D -> E is 4 + 5 + 2 = 11


def test_get_shortest_path(sample_graph):
    path, dist = sample_graph.get_shortest_path("A", "E")
    assert path == ["A", "B", "D", "E"]
    assert dist == 11.0


def test_negative_weight_raises_value_error():
    graph = WeightedGraph()
    with pytest.raises(ValueError, match="Edge weight cannot be negative"):
        graph.add_edge("A", "B", -1.0)


def test_nonexistent_start_node_raises_key_error(sample_graph):
    with pytest.raises(KeyError, match="Start node 'Z' does not exist"):
        sample_graph.dijkstra("Z")


def test_nonexistent_target_node_raises_key_error(sample_graph):
    with pytest.raises(KeyError, match="Target node 'Z' does not exist"):
        sample_graph.get_shortest_path("A", "Z")


def test_unreachable_node():
    graph = WeightedGraph(directed=True)
    graph.add_edge("A", "B", 1)
    graph.add_node("C")  # Disconnected node

    distances, _ = graph.dijkstra("A")
    assert distances["C"] == float("inf")

    path, dist = graph.get_shortest_path("A", "C")
    assert path == []
    assert dist == float("inf")


def test_single_node_graph():
    graph = WeightedGraph()
    graph.add_node("A")

    distances, predecessors = graph.dijkstra("A")
    assert distances["A"] == 0.0
    assert predecessors["A"] is None

    path, dist = graph.get_shortest_path("A", "A")
    assert path == ["A"]
    assert dist == 0.0


def test_undirected_graph():
    graph = WeightedGraph(directed=False)
    graph.add_edge("A", "B", 5)
    graph.add_edge("B", "C", 3)

    path_forward, dist_forward = graph.get_shortest_path("A", "C")
    path_backward, dist_backward = graph.get_shortest_path("C", "A")

    assert path_forward == ["A", "B", "C"]
    assert dist_forward == 8.0
    assert path_backward == ["C", "B", "A"]
    assert dist_backward == 8.0
