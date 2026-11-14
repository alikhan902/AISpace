def solve(n, edges):
    # Create an adjacency list for the graph
    graph = [[] for _ in range(n)]

    # Add edges to the graph
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Check for disconnected graph
    visited = [False] * n
    stack = [0]
    visited[0] = True
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[  neighbor] = True
                stack.append(neighbor)

    # If there's a node not visited, the graph is disconnected
    if any(not v for v in visited):
        raise ValueError

    # Compute eccentricity for each vertex
    eccentricity = [0] * n

    # For each vertex, do BFS to find the farthest node
    for i in range(n):
        # BFS from vertex i
        dist = [-1] * n
        queue = collections.deque()
        queue.append(i)\n        dist[i] = 0
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if dist[neighbor] == -1:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)

        # Find the farthest node from i
        max_dist = max(dist)
        eccentricity[i] = max_dist

    # Find the maximum eccentricity (diameter)
    diameter = max(eccentricity)
    return diameter