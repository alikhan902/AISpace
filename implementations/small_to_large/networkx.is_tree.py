def solve(n, edges):
    if n == 1:
        return True
    if len(edges) != n - 1:
        return False
    # Check connectivity using BFS
    graph = {}
    for u, v in edges:
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)
    visited = set()
    stack = [next(iter(graph.keys()))]
    visited.add(stack[0])
    while stack:
        node = stack.pop()
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    return len(visited) == n