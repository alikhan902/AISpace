from collections import deque

def solve(n, edges):
    if n == 1:
        return True

    color = [ -1 for _ in range(n) ]
    is_bipartite = True

    for start in range(n):
        if color[start] == -1:
            queue = deque([start])
            color[start] = 0

            while queue:
                current = queue.popleft()
                for neighbor in edges[current]:
                    if color[neighbor] == -1:
                        color[neighbor] = color[current] ^ 1
                        queue.append(neighbor)
                    elif color[neighbor] == color[current]:
                        is_bipartite = False
                        break

                if not is_bipartite:
                    break

    return is_bipartite