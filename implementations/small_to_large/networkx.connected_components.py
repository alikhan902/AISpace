def solve(n, edges):
    visited = [False] * n
    components = []

    for i in range(n):
        if not visited[i]:
            # Start BFS from node i
            queue = [i]
            component = []
            visited[i] = True

            while queue:
                node = queue.pop(0)
                component.append(node)

                for neighbor in edges:
                    u, v = neighbor
                    if u == node or v == node:
                        if not visited[v] and u == node:
                            visited[v] = True
                            queue.append(v)
                        elif not visited[u] and v == node:
                            visited[u] = True
                            queue.append(u)

            components.append(component)

    # Sort each component and the list of components lexicographically
    components = [sorted(comp) for comp in components]
    components.sort()
    return components