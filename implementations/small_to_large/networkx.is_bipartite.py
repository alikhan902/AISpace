def solve(n, edges):
    color = [-1] * n  # Initialize color array
    for u in range(n):
        if color[u] == -1:
            # Start BFS from u
            queue = [u]
            color[u] = 0
            while queue:
                current = queue.pop(0)
                for v in edges:
                    if v[0] == current or v[1] == current:
                        neighbor = v[1] if v[0] == current else v[0]
                        if color[neighbor] == -1:
                            color[neighbor] = color[current] ^ 1
                            queue.append(neighbor)
                        elif color[neighbor] != color[current] ^ 1:
                            return False
    return True