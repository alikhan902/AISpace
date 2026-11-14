import sys
from collections import defaultdict
from functools import lru_cache

def solve(n, edges):
    if n == 1:
        return [0]

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n
    discovery = [n] * n
    low = [n] * n
    parent = [-1] * n
    time = 0
    articulation_points = []

    def dfs(u):
        nonlocal time
        visited[u] = True
        discovery[u] = time
        low[u] = time
        time += 1
        children = 0

        for v in graph[u]:
            if not visited[v]:
                parent[v] = u
                children += 1
                dfs(v)
                low[u] = min(low[u], low[v])
                if parent[u] == -1:
                    # Root node
                    if children > 1:
                        articulation_points.append(u)
            else:
                if parent[u] != v:
                    low[u] = min(low[u], discovery[v])

        return

    for u in range(n):
        if not visited[u]:
            dfs(u)

    return sorted(articulation_points)