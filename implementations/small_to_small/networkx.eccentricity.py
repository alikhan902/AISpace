from collections import defaultdict

def solve(n, edges):
    if n == 1:
        return {0}

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Compute all pairs shortest paths using BFS
    eccentricities = {}
    for start in range(n):
        visited = set()
        queue = [(start, 0)]
        while queue:
            node, dist = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, dist + 1))
        # Find maximum distance
        max_dist = 0
        for node in visited:
            max_dist = max(max_dist, dist)
        eccentricities[start] = max_dist

    return eccentricities