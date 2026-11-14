def solve(n, edges):
    # Check that the graph has exactly n-1 edges
    if len(edges) != n - 1:
        return False

    # Check that the graph is connected
    # Build an adjacency list
    adj = {}
    for u, v in edges:
        if u not in adj:
            adj[u] = []
        if v not in adj:
            adj[v] = []
        adj[u].append(v)
        adj[v].append(u)

    # Use BFS to check connectivity
    visited = set()
    queue = collections.deque()
    start_node = next(iter(adj.keys())) if adj else 0
    queue.append(start_node)
    visited.add(start_node)

    while queue:
        node = queue.popleft()
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                visited.add(  neighbor)
                queue.append(neighbor)

    # Check if all nodes are visited
    return len(visited) == n