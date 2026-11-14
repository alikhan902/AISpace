from collections import defaultdict

def solve(n, edges, source):
    graph = defaultdict(int)
    for u, v in edges:
        graph[u] = graph.get(u, 0) + 1
        graph[v] = graph.get(v, 0) + 1

    # Build adjacency list
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # BFS initialization
    visited = set()
    queue = [(source, 0)]
    dist = {source: 0}
    parent = {source: None}

    while queue:
        node, d = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                dist[neighbor] = d + 1
                parent[neighbor] = node
                queue.append((neighbor, d + 1))

    # Build result dictionary
    result = {}
    for node in visited:
        result[node] = dist[node]

    return result