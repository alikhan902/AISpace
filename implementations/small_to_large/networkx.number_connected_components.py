from collections import deque

def solve(n, edges):
    visited = set()
    components = 0
    for i in range(n):
        if i not in visited:
            components += 1
            queue = deque([i])
            visited.add(i)
            while queue:
                node = queue.popleft()
                for neighbor in edges:
                    if neighbor[0] == node or neighbor[1] == node:
                        if neighbor[0] != node:
                            neighbor_node = neighbor[0]
                        else:
                            neighbor_node = neighbor[1]
                        if neighbor_node not in visited:
                            visited.add(neighbor_node)
                            queue.append(neighbor_node)
    return components