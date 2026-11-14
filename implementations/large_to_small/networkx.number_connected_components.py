from collections import deque

def solve(n, edges):
    if n == 0:
        raise ValueError("n must be >= 1")

    visited = [False] * n
    components = 0

    for start in range(n):
        if not visited[start]:
            components += 1
            queue = deque()
            queue.append(start)
            visited[start] = True
            while queue:
                current = queue.popleft()
                for neighbor in range(n):
                    if not visited[neighbor] and (current, neighbor) in edges:
                        visited[neighbor] = True
                        queue.append(neighbor)

    return components