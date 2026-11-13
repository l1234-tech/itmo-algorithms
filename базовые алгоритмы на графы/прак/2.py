def is_bipartite(n, edges) -> bool:
    graph = [[] for _ in range(n)]

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    if len(edges) != n - 1:
        return False

    used = [False] * n
    stack = [0]
    used[0] = True

    while stack:
        versh = stack.pop()

        for neighbor in graph[versh]:
            if not used[neighbor]:
                used[neighbor] = True
                stack.append(neighbor)

    return all(used)
