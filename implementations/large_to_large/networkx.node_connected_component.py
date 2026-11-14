from collections import deque

def solve(n, edges, node):
    # Create an adjacency list for the graph
    graph = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # BFS starting from the given node
    visited = set()
    queue = deque([node])
    visited.add(node)

    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # Convert visited vertices to sorted list of strings
    return sorted([str(v) for v in visited])