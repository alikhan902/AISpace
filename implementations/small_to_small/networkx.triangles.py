from collections import defaultdict

def solve(n, edges):
    triangle_counts = defaultdict(int)
    
    for u, v in edges:
        for w in range(n):
            if w != u and w != v and w < v:
                triangle_counts[w] += 1
    
    return dict(triangle_counts)