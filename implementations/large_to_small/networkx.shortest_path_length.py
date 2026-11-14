from collections import deque

def solve(n, edges, source, target):
    if source == target:
        return 0

    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n
    queue = deque()
    queue.append((source, 0))
    visited[source] = True

    while queue:
        vertex, distance = queue.popleft()
        for neighbor in graph[vertex]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append((neighbor, distance + 1))
                if neighbor == target:
                    return distance + 1

    if not visited[target]:
        raise ValueError("No path exists between source and target")
    return -1