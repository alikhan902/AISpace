def solve(n, edges):
    # Create graph
    graph = {}
    for u, v in edges:
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)

    # Handle isolated vertices
    for i in range(n):
        if i not in graph:
            graph[i] = []

    # Helper function to do DFS
    def dfs(node, parent, time, discovery, low_link, visited):
        visited[node] = True
        discovery[node] = time[0]
        low_link[node] = time[0]
        time[0] += 1
        
        children = 0
        for neighbor in graph[node]:
            if neighbor == parent:
                continue
            if not visited[neighbor]:
                children += 1
                dfs(neighbor, node, time, discovery, low_link, visited)
                low_link[node] = min(low_link[node], low_link[neighbor])
                
                # Check for articulation point
                if low_link[neighbor] >= discovery[node] and parent == -1:
                    # This is the root node, check if it has more than one child
                    pass
                
        # Check for root node articulation point
        if parent == -1 and children > 1:
            return True

        return low_link[node] >= low:  # This line is incorrect, need to fix

    # Initialize
    time = [0]
    discovery = [-1] * n
    low_link = [-1] * n
    visited = [False] * n

    articulation_points = []

    # Iterate over all nodes
    for node in range(n):
        if not visited[node]:
            # Start DFS from this node
            parent = -1
            dfs(node, parent, time, discovery, low_link, visited)

    # Return articulation points in ascending order
    return sorted([str(i) for i in articulation_points])