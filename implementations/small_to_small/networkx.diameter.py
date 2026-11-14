from collections import defaultdict

def solve(n, edges):
    if n == 1:
        return {'0': 0}

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Check if graph is disconnected
    if not graph or not graph[0]:
        raise ValueError

    # Compute eccentricity of each vertex
    eccentricities = {}
    visited = set()

    # BFS to find shortest path from 0
    from collections import deque
    q = deque([0])
    visited.add(0)
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                q.append(v)
                eccentricities[v] = len(visited) - 1

    # BFS to find shortest path from all other vertices
    for v in visited:
        q = deque([v])
        visited_v = set([v])
        while q:
            u = q.popleft()
            for w in graph[u]:
                if w not in visited_v:
                    visited_v.add(w)
                    q.append(w)
                    eccentricities[w] = len(visited_v) - 1

    # Return the diameter (maximum eccentricity)
    if not eccentricities:
        return 0
    return max(eccentricities.values())