def solve(n, edges):
    # If n == 1, there are no edges, so return empty list
    if n == 1:
        return []

    # Create a graph as an adjacency list
    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)

    # Helper function to check if an edge is a bridge
    def is_bridge(u, v):
        # Remove the edge (u, v) from the graph
        graph_copy = graph.copy()
        graph_copy[u] = [x for x in graph_copy[u] if x != v]
        graph_copy[v] = [x for x in graph_copy[v]  if x != u]

        # Perform BFS to count connected components
        visited = set()
        queue = collections.deque([next(iter(graph_copy))])
        visited.add(queue[0])
        while queue:
            node = queue.popleft()
            for neighbor in graph_copy[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        # Count the number of connected components
        num_components = 0
        for node in graph_copy:
            if node not in visited:
                num_components += 1
                queue = collections.deque([node])
                visited.add(node)
                while queue:
                    node = queue.popleft()
                    for neighbor in graph_copy[node]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

        # Original graph has 1 connected component (given the graph is connected)
        # If removing the edge increases the number of components, it's a bridge
        return num_components == 2

    # List to store bridge edges
    bridges = []

    # Iterate through each edge
    for u, v in edges:
        if is_bridge(u, v):
            bridges.append([u, v])

    # Sort lexicographically
    bridges.sort()
    return bridges