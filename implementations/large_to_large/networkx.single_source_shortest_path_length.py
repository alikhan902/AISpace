def solve(n, edges, source):
    # Create an adjacency list for the graph
    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)

    # BFS starting from `source`
    visited = set()
    queue = collections.deque()
    queue.append(source)
    visited.add(source)
    dist = {source: 0}

    while queue:
        current = queue.popleft()
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                dist[neighbor] = dist[current] + 1
                queue.append(neighbor)

    return dist