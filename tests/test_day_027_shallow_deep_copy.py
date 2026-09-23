import copy
import pytest
from learning.python.day_027_shallow_deep_copy import GraphNode, get_graph_nodes

def test_shallow_copy_behavior():
    """Verify that shallow copy duplicates the container but shares nested references."""
    shared_list = [1, 2, 3]
    node_b = GraphNode("B", "valB")
    node_a = GraphNode("A", shared_list, [node_b])

    # Perform shallow copy
    node_a_copy = copy.copy(node_a)

    # Assert node_a_copy is a new object, but shares mutable value and neighbor references
    assert node_a_copy is not node_a
    assert node_a_copy.value is node_a.value
    assert node_a_copy.neighbors is not node_a.neighbors  # The list container itself is copied
    assert node_a_copy.neighbors[0] is node_b  # The elements inside the list are NOT copied

def test_deep_copy_behavior():
    """Verify that deep copy recursively duplicates all nested objects."""
    shared_list = [1, 2, 3]
    node_b = GraphNode("B", "valB")
    node_a = GraphNode("A", shared_list, [node_b])

    # Perform deep copy
    node_a_copy = copy.deepcopy(node_a)

    # Assert node_a_copy and all nested elements are completely independent copies
    assert node_a_copy is not node_a
    assert node_a_copy.value is not node_a.value
    assert node_a_copy.value == node_a.value
    assert node_a_copy.neighbors is not node_a.neighbors
    assert node_a_copy.neighbors[0] is not node_b
    assert node_a_copy.neighbors[0].name == "B"

def test_cyclic_deep_copy():
    """Verify that deep copy handles cyclic references without infinite recursion."""
    node_a = GraphNode("A", "valA")
    node_b = GraphNode("B", "valB")
    
    # Create a cycle: A -> B -> A
    node_a.add_neighbor(node_b)
    node_b.add_neighbor(node_a)

    # Perform deep copy
    node_a_copy = copy.deepcopy(node_a)

    # Verify copy is independent but maintains the cyclic structure
    assert node_a_copy is not node_a
    node_b_copy = node_a_copy.neighbors[0]
    assert node_b_copy is not node_b
    assert node_b_copy.neighbors[0] is node_a_copy  # Cycle preserved in the copied graph

    # Verify total nodes in copied graph
    all_copied_nodes = get_graph_nodes(node_a_copy)
    assert len(all_copied_nodes) == 2
