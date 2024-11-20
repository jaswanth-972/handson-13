from collections import defaultdict

def build_adjacency_map(edges, is_directed):
    """
    Builds an adjacency map (graph representation) from the given edges.
    :param edges: List of tuples representing edges (start, end).
    :param is_directed: Boolean indicating if the graph is directed.
    :return: Adjacency map as a defaultdict of lists.
    """
    adjacency_map = defaultdict(list)
    for origin, destination in edges:
        adjacency_map[origin].append(destination)
        if not is_directed:
            adjacency_map[destination].append(origin)
    return adjacency_map

def perform_dfs(edges, start_point, is_directed=True):
    """
    Performs Depth-First Search (DFS) on a graph.
    :param edges: List of tuples representing the edges of the graph.
    :param start_point: Node to start the DFS traversal.
    :param is_directed: Boolean indicating if the graph is directed.
    """
    # Build the adjacency map
    adjacency_map = build_adjacency_map(edges, is_directed)

    seen = set()  # Tracks visited nodes
    traversal_order = []  # Stores the order of traversal
    cycle_detected = False  # Flag to check for cycles

    def traverse(node, ancestors):
        """Recursive DFS traversal with cycle detection."""
        nonlocal cycle_detected
        if node in seen:
            return
        
        seen.add(node)
        traversal_order.append(node)
        ancestors.add(node)  # Add current node to recursion stack

        for neighbor in adjacency_map[node]:
            if neighbor not in seen:
                traverse(neighbor, ancestors)
            elif is_directed and neighbor in ancestors:
                cycle_detected = True  # Cycle detected in directed graph
            elif not is_directed and neighbor in ancestors:
                # Detect cycles in undirected graphs (back edge)
                if traversal_order[-2] != neighbor:  # Avoid trivial backtracking
                    cycle_detected = True

        ancestors.remove(node)  # Remove node from recursion stack

    # Start DFS from the given start point
    if start_point not in adjacency_map:
        raise ValueError(f"Start point '{start_point}' not found in the graph.")
    
    traverse(start_point, set())

    # Check for disconnected components and traverse them
    all_nodes = set(adjacency_map.keys())
    for node in all_nodes:
        if node not in seen:
            print(f"\nNode '{node}' is part of a disconnected component. Starting DFS for it.")
            traverse(node, set())

    # Output traversal results
    print(f"\nDFS Traversal Order from '{start_point}': {' -> '.join(traversal_order)}")
    if cycle_detected:
        print("Cycle detected in the graph.")
    else:
        print("No cycles detected in the graph.")

# Example Usage
if __name__ == "__main__":
    example_edges = [
        ("u", "v"),
        ("u", "x"),
        ("v", "y"),
        ("y", "x"),
        ("x", "v"),
        ("w", "z"),
        ("w", "y"),
        ("z", "z")  # Self-loop
    ]

    print("Depth-First Search (DFS) from 'u':")
    try:
        perform_dfs(example_edges, 'u', is_directed=True)  # Specify if the graph is directed
    except ValueError as e:
        print(e)
