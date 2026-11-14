from collections import deque

def solve(n, edges):
    if n == 1:
        return True

    visited = set()
    queue = deque([0])
    visited.add(0)

    while queue:
        current = queue.popleft()
        for neighbor in range(n):
            if (current, neighbor) in edges and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited) == n