from collections import deque

def solve(n, edges):
    visited = [False] * n
    components = []

    for start in range(n):
        if not visited[start]:
            queue = deque()
            queue.append(start)
            visited[start] = True
            component = []

            while queue:
                node = queue.popleft()
                component.append(str(node))
                for neighbor in range(n):
                    if not visited[neighbor] and [node, neighbor] in edges:
                        visited[neighbor] = True
                        queue.append(neighbor)

            components.append(sorted(component))

    return sorted(components)