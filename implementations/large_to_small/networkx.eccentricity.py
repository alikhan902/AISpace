from collections import defaultdict

def solve(n, edges):
    if n == 1:
        return {'0': 0}

    # Build the graph
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Check if graph is disconnected
    visited = set()
    queue = [0]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
    if len(visited) != n:
        raise ValueError("Graph is disconnected")

    # Compute shortest paths using BFS
    distances = {}
    for start in range(n):
        dist = {start: 0}
        queue = [start]
        while queue:
            node = queue.pop(0)
            for neighbor in graph[node]:
                if neighbor not in dist:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        distances[start] = max(dist.values())

    # Return the dictionary of eccentricities
    return {str(i): distances[i] for i in range(n)}