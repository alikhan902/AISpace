import collections

def solve(n, edges, node):
    graph = collections.defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    visited = set()
    queue = collections.deque()

    # Start BFS from the specified node
    queue.append(node)
    visited.add(node)

    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited