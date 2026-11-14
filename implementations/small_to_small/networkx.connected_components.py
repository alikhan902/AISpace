from collections import deque

def solve(n, edges):
    if n == 0:
        return []

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
                component.append(node)
                for neighbor in range(n):
                    if not visited[neighbor] and (start, neighbor) in edges or (neighbor, start) in edges:
                        queue.append(neighbor)
                        visited[neighbor] = True

            components.append(set(component))

    # Sort components lexicographically
    components.sort()
    return components