def solve(n, edges):
    if n < 1:
        raise ValueError("n must be at least 1")

    if len(edges) != n - 1:
        raise ValueError("number of edges must be exactly n-1")

    if not all(0 <= u < v < n for u, v in edges):
        raise ValueError("edges must be distinct and valid")

    # Check if the graph is connected
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in graph[node]:
            dfs(neighbor)

    dfs(0)
    if len(visited) != n:
        raise ValueError("graph must be connected")

    # Check if the graph has no cycles
    visited = set()
    in_stack = set()
    def dfs(node):
        if node in in_stack:
            return False
        if node in visited:
            return True
        visited.add(node)
        in_stack.add(node)
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        in_stack.remove(node)
        return True

    if not dfs(0):
        raise ValueError("graph must be acyclic")

    return 1