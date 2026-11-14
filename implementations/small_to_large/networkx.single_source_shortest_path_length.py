def solve(n, edges, source):
    # Initialize distances to infinity
    dist = {i: float('inf') for i in range(n)}
    
    # Set distance to source as 0
    dist[source] = 0
    
    # Create a priority queue for Dijkstra's algorithm
    heap = [(0, source)]
    
    # Process nodes in order of increasing distance
    while heap:
        d, node = heapq.heappop(heap)
        
        # If we have a better distance, skip
        if d != dist[node]:
            continue
        
        # Relax edges from this node
        for u, v in edges:
            if u == node:
                new_dist = dist[node] + 1
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(heap, (new  # ... (truncated)
    return dist