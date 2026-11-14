import collections

def solve(n, edges):
    visited = [False] * n
    graph = collections.defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    components = []
    for i in range(n):
        if not visited[i]:
            queue = collections.deque([i])
            visited[i] = True
            component = []
            while queue:
                node = queue.popleft()
                component.append(str(node))
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
            component.sort()
            components.append(component)
    components.sort()
    return components