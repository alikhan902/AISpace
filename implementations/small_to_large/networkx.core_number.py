def solve(n, edges):
    # Initialize core numbers to 0 for all nodes
    core = {i: 0 for i in range(n)}

    # Create a degree count for each node
    degree = [0] * n

    # Count the degree of each node
    for u, v in edges:
        degree[u] += 1
        degree[v] += .5

    # We'll use a queue to process nodes with current degree less than k
    # Start with k = 1
    k = 1

    # We need to process nodes with degree less than k
    # We'll maintain a list of nodes with current degree less than k
    # For k=1, we want nodes with degree < 1 (i.e., degree 0)
    # But note: the degree we computed is the actual degree
    # However, the above degree calculation is incorrect because we are using .5 for v
    # Let's fix: we should use integer degrees

    # Correct degree calculation
    degree = [0] * n
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1

    # Now, we'll use a queue for nodes with current degree less than k
    # We start with k=1
    # We'll maintain a list of nodes with current degree < k
    # For k=1, we want nodes with degree < 1 (i.e., degree 0)
    # But note: the core number algorithm is iterative

    # We'll use a queue for nodes with current degree < k
    # We start with k=1
    # We'll maintain a list of nodes with current degree < k
    # For k=1, we want nodes with degree < 1 (i.e., degree 0)
    # However, the standard algorithm is:
    #   Let core = [0] * n
    #   Let deg = [degree of each node]
    #   Queue all nodes with deg[i] < 1 (i.e., deg[i] == 0)
    #   While queue not empty:
    #       pop node u
    #       for each neighbor v of u:
    #           deg[v] -= 1
    #           if deg[v] < k:
    #               push v
    #       k += 1
    #   But note: the core number for a node is the largest k such that the node is in a k-core
    #   So we need to track the core number as we go

    # We'll do:
    #   core = [0] * n
    #   deg = [degree of each node]
    #   queue = deque([i for i in range(n) if deg[i] == 0])
    #   k = 1
    #   while queue:
    #       for _ in range(len(queue)):
    #           u = queue.popleft()
    #           for v in graph[u]:
    #               deg[v] -= 1
    #               if deg[v] < k:
    #                   queue.append(v)
    #       k += 1
    #   But note: the core number for a node is the k at which it was removed
    #   However, the standard algorithm returns the core number as the k when the node is removed
    #   But the problem says: for each node, determine the largest k for which the node is in a k-core
    #   So the core number is the k at which the node is removed

    # However, the problem states: the graph must be simple and undirected, and edges are distinct with 0<=u<v<n

    # We need to build the graph
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Now, we'll use a queue for nodes with current degree < k
    # We start with k=1
    # We want to find all nodes with degree < 1 (i.e., degree 0)
    # But note: the core number algorithm is iterative
    # We'll maintain a list of nodes with current degree < k
    # For k=1, we want nodes with degree < 1 (i.e., degree 0)
    # However, the standard algorithm uses a queue for nodes with degree < k
    # We'll do:
    #   core = [0] * n
    #   deg = degree (list of current degrees)
    #   queue = deque([i for i in range(n) if deg[i] == 0])
    #   k = 1
    #   while queue:
    #       for _ in range(len(queue)):
    #           u = queue.popleft()
    #           core[u] = k - 1  # because when we remove u, it's part of the (k-1)-core
    #           for v in graph[u]:
    #               deg[v] -= 1
    #               if deg[v] < k:
    #                   queue.append(v)
    #       k += 1
    #   But note: the problem says the core number is the largest k for which the node is in a k-core
    #   So for a node that is removed at step k, its core number is k-1
    #   However, the problem states: for k=1,2,...,n
    #   The core number for a node is the largest k such that the node is in a k-core
    #   So the algorithm above sets core[u] = k-1 when u is removed
    #   But the problem says: when the graph is empty, all nodes have core number 0
    #   So for a node with degree 0, it is removed at k=1, so core number = 0
    #   This matches

    # However, the problem says: the graph must be connected or contain isolated vertices
    # We'll implement the algorithm

    # But note: the problem says the graph is simple and undirected, so we don't have self loops or multiple edges

    # Steps:
    #   1. Build graph
    #   2. Compute initial degrees
    #   3. Initialize a queue with nodes that have degree 0
    #   4. Set k = 1
    #   5. While queue is not empty:
    #        - Process all nodes in the current queue (for the current k)
    #        - For each node u in the queue:
    #             - Set core[u] = k - 1
    #             - For each neighbor v of u:
    #                 - deg[v] -= 1
    #                 - If deg[v] < k, then add v to the queue for the next k
    #        - k += 1
    #   6. Return core as a dictionary

    # However, note: the problem says the output is a dictionary mapping every string vertex key to its integer core number
    # But the input vertices are integers (0 to n-1)
    # The problem says: 