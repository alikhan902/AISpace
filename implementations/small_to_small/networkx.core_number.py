from collections import defaultdict

def solve(n, edges):
    # Create adjacency list
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Compute degree of each node
    degrees = [len(adj[u]) for u in range(n)]

    # Compute k-core subgraphs for k = 1, 2, ..., n
    core_numbers = [0] * n

    # For each node, determine the largest k for which it is in a k-core
    for u in range(n):
        k = 1
        while k <= n and degrees[u] >= k:
            k += 1
        core_numbers[u] = k - 1

    return {str(i): core_numbers[i] for i in range(n)}