from collections import defaultdict

def solve(n, edges):
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    triangle_counts = {}
    for i in range(n):
        count = 0
        neighbors = list(graph[i])
        for j in range(len(neighbors)):
            for k in range(j + 1, len(neighbors)):
                if neighbors[j] in graph[neighbors[k]]:
                    count += 1
        triangle_counts[str(i)] = count
    return triangle_counts