from collections import defaultdict

def solve(n, edges, source):
    graph = defaultdict(lambda: 0)
    for u, v in edges:
        graph[u] = min(graph[u], 1)
        graph[v] = min(graph[v], 1)

    dist = {source: 0}
    queue = [source]

    while queue:
        current = queue.pop(0)
        for neighbor in graph.keys():
            if graph[neighbor] == graph[current] + 1 and neighbor not in dist:
                dist[neighbor] = graph[neighbor]
                queue.append(neighbor)

    return dist