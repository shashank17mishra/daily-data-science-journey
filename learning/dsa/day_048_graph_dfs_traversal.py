import collections

def dfs_traversal(graph: dict[str, list[str]], start_node: str) -> list[str]:
    """
    Performs a Depth-First Search (DFS) traversal on a graph starting from a given node.

    The graph is represented using an adjacency list. This implementation uses a
    recursive approach to explore as far as possible along each branch before backtracking.

    Args:
        graph: An adjacency list representation of the graph where keys are nodes
               and values are lists of their neighbors. It's assumed to be an
               undirected graph for typical traversal behavior, meaning if 'A' is
               connected to 'B', then 'B' is also connected to 'A' (represented
               in the adjacency list for both 'A' and 'B').
        start_node: The node from which to start the DFS traversal.

    Returns:
        A list of nodes in the order they were visited during the DFS traversal.
        Returns an empty list if the start_node is not present as a key in the graph.
    """
    # If the start_node is not a key in the graph, it means it has no outgoing edges
    # and cannot initiate a traversal to other nodes. Return an empty list.
    if start_node not in graph:
        return []

    visited = set()
    traversal_order = []

    def dfs_recursive(node):
        """Helper recursive function for DFS."""
        visited.add(node)
        traversal_order.append(node)

        # Iterate through neighbors. graph.get(node, []) handles cases where a node
        # might be a key but have no neighbors (empty list).
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs_recursive(neighbor)

    dfs_recursive(start_node)
    return traversal_order


if __name__ == "__main__":
    # Example Usage:
    print("--- Example 1: Simple Path ---")
    graph1 = {
        'A': ['B'],
        'B': ['A', 'C'],
        'C': ['B', 'D'],
        'D': ['C']
    }
    print(f"Graph: {graph1}")
    print(f"DFS from 'A': {dfs_traversal(graph1, 'A')}") # Expected: ['A', 'B', 'C', 'D']

    print("\n--- Example 2: Branched Graph ---")
    graph2 = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'E'],
        'D': ['B'],
        'E': ['C']
    }
    print(f"Graph: {graph2}")
    print(f"DFS from 'A': {dfs_traversal(graph2, 'A')}") # Expected: ['A', 'B', 'D', 'C', 'E'] (order depends on adjacency list order)

    print("\n--- Example 3: Graph with Cycle ---")
    graph3 = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['B', 'C']
    }
    print(f"Graph: {graph3}")
    print(f"DFS from 'A': {dfs_traversal(graph3, 'A')}") # Expected: ['A', 'B', 'D', 'C']

    print("\n--- Example 4: Disconnected Graph ---")
    graph4 = {
        '1': ['2'],
        '2': ['1'],
        'A': ['B'],
        'B': ['A']
    }
    print(f"Graph: {graph4}")
    print(f"DFS from '1': {dfs_traversal(graph4, '1')}") # Expected: ['1', '2']
    print(f"DFS from 'A': {dfs_traversal(graph4, 'A')}") # Expected: ['A', 'B']

    print("\n--- Example 5: Start node not in graph ---")
    graph5 = {'X': ['Y']}
    print(f"Graph: {graph5}")
    print(f"DFS from 'Z': {dfs_traversal(graph5, 'Z')}") # Expected: []
