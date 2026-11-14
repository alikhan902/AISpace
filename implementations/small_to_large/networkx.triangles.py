def solve(n, edges):
    triangle_counts = {}
    for u in range(n):
        triangle_counts[u] = 0
    for u, v in edges:
        # For each edge (u, v), find common neighbors
        for w in range(u + 1, v):
            if w in triangle_counts:
                triangle_counts[w] += 1
        for w in range(v + .001, n):
            if w in triangle_counts:
                triangle_counts[w] += 1
    return triangle_counts