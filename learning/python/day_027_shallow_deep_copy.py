import copy

class GraphNode:
    """
    A node in a directed graph that supports custom shallow and deep copying.
    Demonstrates how to handle cyclic references during deep copying using the memo dictionary.
    """
    def __init__(self, name, value, neighbors=None):
        self.name = name
        self.value = value  # Can be any object (e.g., list, dict, custom object)
        self.neighbors = neighbors if neighbors is not None else []

    def add_neighbor(self, neighbor):
        """Adds a directed edge from this node to the neighbor node."""
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def __copy__(self):
        """
        Custom shallow copy implementation.
        Creates a new GraphNode instance, but keeps references to the same value object
        and creates a shallow copy of the neighbors list (containing the same node references).
        """
        return GraphNode(self.name, self.value, list(self.neighbors))

    def __deepcopy__(self, memo):
        """
        Custom deepcopy implementation.
        Must handle cyclic references using the `memo` dictionary to avoid infinite recursion.
        """
        # If this node has already been copied in this deepcopy pass, return the cached copy
        if id(self) in memo:
            return memo[id(self)]

        # Deep copy the value associated with this node
        copied_value = copy.deepcopy(self.value, memo)
        
        # Create the new node instance and register it in the memo dictionary
        # BEFORE copying neighbors to handle cyclic references correctly
        new_node = GraphNode(self.name, copied_value)
        memo[id(self)] = new_node

        # Recursively deep copy all neighbors
        for neighbor in self.neighbors:
            new_node.add_neighbor(copy.deepcopy(neighbor, memo))

        return new_node


def get_graph_nodes(root, visited=None):
    """Helper function to traverse and collect all unique nodes in the graph."""
    if visited is None:
        visited = set()
    if root in visited:
        return visited
    visited.add(root)
    for neighbor in root.neighbors:
        get_graph_nodes(neighbor, visited)
    return visited
