from collections import deque

def solve(n, edges):
    if n == 1:
        return True
    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)
    visited = set()
    queue = deque()
    start_node = 0
    queue.append(start_node)
    visited.add(start_node)
    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return len(visited) == n