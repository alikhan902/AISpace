from collections import deque

def solve(n, edges):
    if n == 0:
        return 0

    visited = set()
    components = 0

    # Create an adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # BFS traversal
    for i in range(n):
        if i not in visited:
            components += 1
            queue = deque()
            queue.append(i)
            visited.add(i)
            while queue:
                node = queue.popleft()
                for neighbor in adj[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

    return components