def solve(n, edges, source, target):
    if source == target:
        return 0
    
    # Build graph as adjacency list
    graph = {}
    for u in range(n):
        graph[u] = []
    
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # BFS from source
    visited = [False] * n
    queue = collections.deque()
    queue.append(source)
    visited[source] = True
    distance = [-1] * n
    distance[source] = 0
    
    while queue:
        current = queue.popleft()
        if current == target:
            return distance[current]
        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                distance[neighbor] = distance[current] + 1
                queue.append(neighbor)
    
    raise ValueError("No path from source to target")