import sys
from collections import defaultdict
from functools import lru_cache

def solve(n, edges):
    if n == 0:
        return []

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n
    parent = [-1] * n
    disc = [0] * n
    low = [0] * n
    time = 0
    bridges = []

    def dfs(u):
        nonlocal time
        visited[u] = True
        disc[u] = time
        low[u] = time
        time += 1
        children = 0

        for v in graph[u]:
            if not visited[v]:
                parent[v] = u
                children += 1
                dfs(v)
                low[u] = min(low[u], low[v])
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

        if parent[u] != -1 and low[v] >= disc[u]:
            bridges.append((u, v))

    for u in range(n):
        if not visited[u]:
            dfs(u)

    return bridges