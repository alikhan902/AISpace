def solve(n, edges, node):
    # Create an adjacency list for the graph
    graph = {}
    for u, v in edges:
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)

    # BFS starting from the specified node
    visited = set()
    queue = collections.deque([node])
    visited.add(node)

    while queue:
        current = queue.popleft()
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited