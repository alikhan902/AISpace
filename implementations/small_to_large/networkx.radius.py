import collections

def solve(n, edges):
    if n == 1:
        return 0

    # Build the graph
    graph = collections.defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Compute the eccentricity for each vertex
    eccentricities = {}
    for vertex in range(n):
        # BFS from this vertex
        queue = collections.deque()
        queue.append((vertex, 0))
        visited = set()
        visited.add(vertex)
        while queue:
            current, dist = queue.popleft()
            if current not in graph:
                # This vertex has no neighbors, so we're done
                continue
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        # The eccentricity is the maximum distance from this vertex
        eccentricities[vertex] = max(dist for dist in [d for (v, d) in queue] + [0])

    # Find the minimum eccentricity
    min_eccentricity = min(eccentric  for ecc in eccentricities.values())
    return min_eccentricity