import sys
from collections import defaultdict
from functools import lru_cache

def solve(n, edges):
    if n == 1:
        return []

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    disc = {}
    low = {}
    time = 0
    parent = {}
    is_articulation = {}
    in_stack = {}

    def dfs(u):
        nonlocal time
        disc[u] = time
        low[u] = time
        time += 1
        in_stack[u] = True
        visited.add(u)
        parent[u] = parent.get(u, -1)

        for v in graph[u]:
            if v == parent[u]:
                continue

            if v not in visited:
                dfs(v)
                low[u] = min(low[u], low[v])

                if parent[u] == -1:
                    low[u] = min(low[u], disc[u])
                elif low[v] > disc[u]:
                    is_articulation[u] = True
            else:
                low[u] = min(low[u], disc[v])

        in_stack[u] = False

    for u in range(n):
        if u not in visited:
            dfs(u)

    result = []
    for u in range(n):
        if is_articulation[u] and u not in visited:
            result.append(u)

    return sorted(str(u) for u in result)