def solve(n, edges):
    # Construct graph
    graph = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Find connected components
    visited = [False] * n
    components = []
    for i in range(n):
        if not visited[i]:
            comp = []
            stack = [i]
            visited[i] = True
            while stack:
                node = stack.pop()
                comp.append(node)
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)
            components.append(comp)

    # For each component, find bridges
    bridges = []
    for comp in components:
        # Build subgraph for the component
        comp_graph = {node: [] for node in comp}
        for node in comp:
            for neighbor in graph[node]:
                if neighbor in comp:
                    comp_graph[node].append(neighbor)

        # Use DFS to find bridges (Tarjan's algorithm)
        visited_comp = [False] * len(comp)
        disc = [-1] * len(comp)
        low = [-1]  * len(comp)
        parent = [-1] * len(comp)
        time = 0

        def dfs(u, parent_u):
            nonlocal time
            disc[u] = time
            low[u] = time
            time += 1
            for v in comp_graph[u]:
                if v == parent_u:
                    continue
                if disc[v] == -1:
                    parent[v] = u
                    dfs(v, u)
                    low[u] = min(low[u], low[v])
                    if low[v] > disc[u]:
                        # Bridge found
                        bridges.append((min(u, v), max(u, v)))
                else:
                    low[u] = min(low[u], disc[v])

        # Start DFS for each node in the component
        for idx, node in enumerate(comp):
            if not visited_comp[idx]:
                visited_comp[idx] = True
                dfs(idx, -1)

    # Sort bridges lexicographically by (u, v) with u < v
    bridges.sort(key=lambda x: (x[0], x[1]))
    return bridges