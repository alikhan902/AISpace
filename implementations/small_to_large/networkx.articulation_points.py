def solve(n, edges):
    if n == 1:
        return [0]
    graph = {}
    for u, v in edges:
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)
    visited = [False] * n
    discovery_time = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    ap = [False] * n
    time = 0

    def dfs(u):
        nonlocal time
        visited[u] = True
        discovery_time[u] = time
        low[u] = time
        time += 1
        children = 0
        for v in graph.get(u, []):
            if not visited[v]:
                parent[v] = u
                children += 1
                dfs(v)
                low[u] = min(low[u], discovery_time[v])
                # Check if u is an articulation point
                if low[v] >= discovery_time[u] and parent[u] == -1:
                    ap[u] = True
            elif v != parent[u]:
                low[u] = min(low[u], discovery_time[v])

        # After processing all children, check for articulation point
        if parent[u] == -1 and children > 1:
            ap[u] = True
        elif parent[u] != -1 and low[u] >= discovery_time[u]:
            ap[u] = True

    for i in range(n):
        if not visited[i]:
            dfs(i)

    return [i for i in range(n) if ap[i]]