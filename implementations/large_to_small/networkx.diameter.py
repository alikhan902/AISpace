import math

def solve(n, edges):
    if n == 1:
        return 0

    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Compute eccentricity for each vertex
    eccentricities = [0] * n

    for i in range(n):
        # Compute shortest path to all other nodes
        dist = [math.inf] * n
        dist[i] = 0
        queue = [i]
        while queue:
            u = queue.pop(0)
            for v in adj[u]:
                if dist[v] > dist[u] + 1:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        # Compute eccentricity
        max_dist = max(dist)
        eccentricities[i] = max_dist

    # Find maximum eccentricity
    max_eccentricity = max(eccentricities)
    return max_eccentricity