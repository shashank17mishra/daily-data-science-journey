from collections import deque

def bfs_traversal(graph: dict, start_node) -> list:
    """
    Performs a Breadth-First Search (BFS) traversal on a graph starting from a given node.

    Args:
        graph (dict): An adjacency list representation of the graph.
                      Keys are nodes, values are lists of their neighbors.
                      Example: {0: [1, 2], 1: [2], 2: [0, 3], 3: [3]}
        start_node: The node from which to start the BFS traversal.

    Returns:
        list: A list of nodes in the order they were visited during BFS.
              Returns an empty list if the start_node is not in the graph
              or if the graph is empty.
    """
    if not graph or start_node not in graph:
        return []

    visited = set()
    queue = deque()
    traversal_order = []

    # Start BFS from the initial node
    queue.append(start_node)
    visited.add(start_node)

    while queue:
        current_node = queue.popleft()
        traversal_order.append(current_node)

        # Explore neighbors
        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return traversal_order
