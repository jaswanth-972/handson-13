class GraphEdge:
    def __init__(self, weight, start, end):
        """
        Initializes a GraphEdge instance representing an edge in the graph.
        
        :param weight: The weight of the edge.
        :param start: The starting vertex of the edge.
        :param end: The ending vertex of the edge.
        """
        self.weight = weight
        self.start = start
        self.end = end

    def __repr__(self):
        """
        Returns a string representation of the edge in the format:
        start --(weight)--> end
        """
        return f"{self.start} --({self.weight})--> {self.end}"


class DisjointSetUnion:
    def __init__(self, vertices):
        """
        Initializes the Disjoint Set Union (DSU) or Union-Find data structure.
        
        :param vertices: A set of vertices in the graph.
        """
        self.parent = {vertex: vertex for vertex in vertices}  # Parent of each vertex
        self.rank = {vertex: 0 for vertex in vertices}  # Rank for union by rank optimization

    def find(self, vertex):
        """
        Find the representative of the set containing the vertex with path compression.
        
        :param vertex: The vertex whose set representative we want to find.
        :return: The representative (or root) of the set containing the vertex.
        """
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])  # Path compression
        return self.parent[vertex]

    def union(self, vertex1, vertex2):
        """
        Unites the sets containing vertex1 and vertex2 using union by rank.
        
        :param vertex1: The first vertex.
        :param vertex2: The second vertex.
        """
        root1 = self.find(vertex1)
        root2 = self.find(vertex2)
        
        if root1 != root2:  # Only union if they are in different sets
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1


def kruskal_mst(vertices, edges):
    """
    Finds the Minimum Spanning Tree (MST) using Kruskal's algorithm.
    
    :param vertices: A set of vertices in the graph.
    :param edges: A list of GraphEdge objects representing the edges of the graph.
    :return: A tuple containing the list of MST edges and the total weight of the MST.
    """
    if not vertices or not edges:
        print("Error: The graph must have at least one vertex and one edge.")
        return [], 0

    # Sort edges by weight in ascending order
    edges = sorted(edges, key=lambda edge: edge.weight)
    
    dsu = DisjointSetUnion(vertices)  # Disjoint Set Union instance
    mst_result = []  # List to store the edges of the MST
    total_weight = 0  # Variable to store the total weight of the MST

    for edge in edges:
        # If the edge doesn't form a cycle, add it to the MST
        if dsu.find(edge.start) != dsu.find(edge.end):
            dsu.union(edge.start, edge.end)  # Union the two vertices
            mst_result.append(edge)  # Add the edge to MST
            total_weight += edge.weight  # Add the edge weight to the total

    # Check if the graph is connected (i.e., there is a spanning tree)
    connected_components = set(dsu.find(vertex) for vertex in vertices)
    if len(connected_components) > 1:
        print("\nWarning: The graph is disconnected. MST includes only connected components.")
        print(f"Number of connected components: {len(connected_components)}")

    return mst_result, total_weight


if __name__ == "__main__":
    # Define nodes and edges for Kruskal's example
    nodes_kruskal = {"a", "b", "c", "d", "e", "f", "g", "h", "i"}
    edges_kruskal = [
        GraphEdge(4, "a", "b"),
        GraphEdge(8, "a", "h"),
        GraphEdge(8, "b", "c"),
        GraphEdge(11, "b", "h"),
        GraphEdge(7, "c", "d"),
        GraphEdge(4, "c", "f"),
        GraphEdge(2, "c", "i"),
        GraphEdge(6, "c", "g"),
        GraphEdge(9, "d", "e"),
        GraphEdge(14, "d", "f"),
        GraphEdge(10, "e", "f"),
        GraphEdge(2, "f", "g"),
        GraphEdge(1, "g", "h"),
        GraphEdge(7, "h", "i")
    ]

    # Perform Kruskal's MST
    mst, total_weight = kruskal_mst(nodes_kruskal, edges_kruskal)

    # Output results
    if mst:
        print("\nEdges in Kruskal's MST:")
        for edge in mst:
            print(edge)
        print(f"\nTotal weight of MST: {total_weight}")
    else:
        print("No MST could be formed due to insufficient edges or invalid input.")
