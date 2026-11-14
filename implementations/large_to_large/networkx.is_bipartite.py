def solve(n, edges):
    # Create an adjacency list for the graph
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Color array to store color of each vertex (0 or 1)
    color = [-1] * n

    # Helper function to check if the graph is bipartite
    def is_bipartite(start):
        queue = [start]
        color[start] = 0
        while queue:
            current = queue.pop(0)
            for neighbor in graph[current]:
                if color[neighbor] == -1:
                    color[neighbor] = color[current] ^ 1
                    queue.append(neighbor)
                elif color[neighbor] == color[current]:
                    return False
        return True

    # Check each connected component
    for i in range(n):
        if color[i] == -1:
            if not is_bipartite(i):
                return False
    return True