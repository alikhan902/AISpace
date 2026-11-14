import collections

def solve(n, edges):
    # Step 1: Construct the graph
    graph = collections.defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Step : Check for disconnected graph
    visited = set()
    for node in range(n):
        if node not in visited:
            stack = [node]
            visited.add(node)
            while stack:
                current = stack.pop()
                for neighbor in graph.get(current, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
    if len(visited) != n:
        raise ValueError("Graph is disconnected")

    # Step 2: Compute shortest path distances for each vertex
    eccentricities = {}
    for start in range(n):
        # BFS from start
        dist = [-1] * n
        queue = collections.deque()
        queue.append(start)\n        dist[start] = 0
        while queue:
            current = queue.popleft()
            for neighbor in graph.get(current, []):
                if dist[neighbor] == -1:
                    dist[neighbor] = dist[current] + 1
                    queue.append(neighbor)
        # Find the maximum distance from start
        max_dist = max(dist)
        eccentricities[str(start)] = max_dist

    return eccentricities