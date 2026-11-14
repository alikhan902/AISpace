from collections import deque

def solve(n, edges):
    if n == 0:
        return 0

    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # BFS traversal
    visited = [False] * n
    queue = deque()
    queue.append(0)
    visited[0] = True

    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if not visited[neighbor] and neighbor != 0:
                visited[neighbor] = True
                queue.append(neighbor)

    # Check if all nodes are visited
    return 1 if all(visited[i] for i in range(n)) else 0