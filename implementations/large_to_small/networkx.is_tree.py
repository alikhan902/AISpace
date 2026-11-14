def solve(n, edges):
    if n < 1:
        raise ValueError("n must be at least 1")

    if len(edges) != n - 1:
        raise ValueError("graph must have exactly n-1 edges")

    if not isinstance(edges, list):
        raise ValueError("edges must be a list")

    if not all(0 <= u < v < n for u, v in edges):
        raise ValueError("edges must be distinct and unordered pairs with u < v")

    if not all(len(edge) == 2 for edge in edges):
        raise ValueError("edges must be pairs")

    if not all(isinstance(edge, int) for edge in edges):
        raise ValueError("edges must be integers")

    # Check if the graph is connected
    if not is_connected(edges, n):
        return False

    # Check if the graph is acyclic
    if not is_acyclic(edges, n):
        return False

    return True

def is_connected(edges, n):
    if n == 1:
        return True

    visited = set()
    queue = [0]
    while queue:
        u = queue.pop(0)
        if u in visited:
            continue
        visited.add(u)
        for v in range(n):
            if v not in visited and (u, v) in edges:
                queue.append(v)
    return len(visited) == n

def is_acyclic(edges, n):
    if n == 1:
        return True

    visited = set()
    stack = [0]
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        for v in range(n):
            if v not in visited and (u, v) in edges:
                stack.append(v)
    return len(visited) == n