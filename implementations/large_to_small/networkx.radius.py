import functools

def solve(n, edges):
    if n == 1:
        return 0

    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Compute shortest path distances from each node
    dist = [functools.reduce(lambda x, y: x + y, [0] * n, 0)]  # Initialize with 0 for all
    for i in range(n):
        queue = [i]
        dist[i] = 0
        while queue:
            u = queue.pop(0)
            for v in adj[u]:
                if dist[v] == 0:
                    dist[v] = dist[u] + 1
                    queue.append(v)

    # Compute eccentricity for each node
    ecc = [0] * n
    for i in range(n):
        max_dist = 0
        for j in range(n):
            if dist[j] > max_dist:
                max_dist = dist[j]
        ecc[i] = max_dist

    # Find the minimum eccentricity
    return min(ecc)