from collections import defaultdict

class DirectedGraph:
    def __init__(self):
        """Initialize an empty graph using an adjacency list."""
        self.adjacency_list = defaultdict(list)

    def insert_edge(self, start, end):
        """Add a directed edge from `start` to `end`."""
        self.adjacency_list[start].append(end)

    def _topological_sort_helper(self, node, visited, recursion_stack, sorted_nodes):
        """
        Recursive helper function for topological sort.
        Detects cycles and performs depth-first traversal.
        """
        visited[node] = True
        recursion_stack[node] = True  # Mark the node as part of the current recursion stack

        for neighbor in self.adjacency_list[node]:
            if not visited[neighbor]:
                if not self._topological_sort_helper(neighbor, visited, recursion_stack, sorted_nodes):
                    return False  # Cycle detected
            elif recursion_stack[neighbor]:
                # If a neighbor is in the recursion stack, there's a cycle
                print(f"Cycle detected: Node '{neighbor}' is part of a cycle.")
                return False

        recursion_stack[node] = False  # Remove the node from the recursion stack
        sorted_nodes.append(node)  # Append node to the sorted list
        return True

    def compute_topological_sort(self, vertices):
        """
        Perform topological sort on the graph.
        Returns the sorted order or None if a cycle is detected.
        """
        visited = {vertex: False for vertex in vertices}
        recursion_stack = {vertex: False for vertex in vertices}
        sorted_nodes = []

        for vertex in vertices:
            if not visited[vertex]:
                if not self._topological_sort_helper(vertex, visited, recursion_stack, sorted_nodes):
                    return None  # Cycle detected

        sorted_nodes.reverse()  # Reverse the list to get the correct order
        return sorted_nodes


# Example Usage
if __name__ == "__main__":
    # Define vertices and edges for the example
    vertices = ["undershorts", "pants", "belt", "shirt", "tie", "jacket", "socks", "shoes", "watch"]

    # List of directed edges
    connections = [
        ("undershorts", "pants"),
        ("pants", "belt"),
        ("pants", "shoes"),
        ("shirt", "belt"),
        ("shirt", "tie"),
        ("tie", "jacket"),
        ("belt", "jacket"),
        ("socks", "shoes")
    ]

    # Create graph and add edges
    graph = DirectedGraph()
    for start, end in connections:
        graph.insert_edge(start, end)

    # Check for disconnected vertices and warn if any
    missing_vertices = set(vertices) - set(graph.adjacency_list.keys())
    if missing_vertices:
        print(f"Warning: The following vertices have no outgoing edges: {', '.join(missing_vertices)}")

    # Perform topological sort
    result = graph.compute_topological_sort(vertices)

    if result:
        print("Topological Sort:", result)
    else:
        print("The graph contains a cycle and cannot be topologically sorted.")
