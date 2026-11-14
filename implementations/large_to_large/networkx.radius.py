import heapq
from collections import deque


def solve(n, edges):
    # Check if the graph is connected
    if n == 1:
        return 0

    # Build the graph
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Check for disconnected graph
    visited = [False] * n
    queue = deque([0])
    visited[0] = True
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

    if not all(visited):
        raise ValueError("Graph is disconnected")

    # Compute eccentricity for each vertex
    eccentricities = [0] * n
    for start in range(n):
        # BFS from start to compute shortest path distances
        dist = [-1] * n
        queue = deque([start])
        dist[start] = 0
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if dist[neighbor] == -1:
                    dist[  neighbor] = dist[node] + 1
                    queue.append(neighbor)
        # Find maximum distance (eccentricity)
        ecc = max(dist)
        eccentricities[start] = ecc

    # Find the minimum eccentricity (radius)
    radius = min(eccentricities)
    return radius