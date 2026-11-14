import heapq

def solve(n, edges, source, target):
    # Build the graph
    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)

    # Dijkstra's algorithm
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    visited = set()
    heap = [(0, source)]

    while heap:
        current_dist, current_node = heapq.heappop(heap)
        if current_node in visited:
            continue
        visited.add(current_node)
        if current_node == target:
            return current_dist
        for neighbor in graph[current_node]:
            if dist[neighbor] > current_dist + 1:
                dist[neighbor] = current_dist + 1
                heapq.heappush(heap, (dist[neighbor], neighbor))

    # No path found
    if target not in dist:
        raise ValueError("No path exists between source and target")
    return dist[target)