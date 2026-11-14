import collections

def solve(n, edges):
    if n == 1:
        return True

    graph = collections.defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    color = collections.defaultdict(int)
    is_bipartite = True

    for start in range(n):
        if color[start] == 0:
            queue = collections.deque([start])
            color[start] = 1

            while queue:
                current = queue.popleft()
                for neighbor in graph[current]:
                    if color[neighbor] == 0:
                        color[neighbor] = color[current] ^ 1
                        queue.append(neighbor)
                    elif color[neighbor] == color[current]:
                        is_bipartite = False
                        break

                if not is_bipartite:
                    break

    return is_bipartite