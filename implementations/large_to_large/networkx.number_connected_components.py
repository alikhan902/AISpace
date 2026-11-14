def solve(n, edges):
    # Create an adjacency list for the graph
    graph = {i: [] for i in range(n)}

    # Build the graph from edges
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Track visited vertices
    visited = [False] * n

    # Count connected components
    count = 0

    # Iterate over each vertex
    for i in range(n):
        if not visited[i]:
            count += 1
            # BFS to mark all reachable vertices
            queue = [i]
            visited[i] = True
            while queue:
                current = queue.pop(0)
                for neighbor in graph[current]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)

    return count