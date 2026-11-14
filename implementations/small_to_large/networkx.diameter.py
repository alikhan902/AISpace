def solve(n, edges):
    if n == 1:
        return 0

    # Build adjacency list
    adj = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Check for disconnected graph
    visited = set()
    stack = [0]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    stack.append(neighbor)

    if len(visited) != n:
        raise ValueError("Graph is disconnected")

    # Compute eccentricity for each vertex
    eccentricities = {}
    for node in range(n):
        # BFS from this node
        dist = {node: 0}
        queue = collections.deque([node])
        while queue:
            current = queue.popleft()
            for neighbor in adj[current]:
                if neighbor not in dist:
                    dist[neighbor] = dist[current] + 1
                    queue.append(neighbor)
        # Eccentricity is max distance from this node
        ecc = max(dist.values()) if dist else 0
        eccentricities[str(node)] = ecc

    # Find the diameter (max eccentricity)
    diameter = max(eccentricities.values())
    return diameter