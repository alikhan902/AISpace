from collections import deque

def solve(n, edges):
    if n == 1:
        return {0: 0}

    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    eccentricities = {}
    for start in range(n):
        # BFS from start
        dist = [-1] * n
        queue = deque()
        queue.append(start)\n        dist[start] = 0
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if dist[neighbor] == -1:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        # Find max distance
        max_dist = max(dist)
        eccentricities[start] = max_dist

    return eccentricities