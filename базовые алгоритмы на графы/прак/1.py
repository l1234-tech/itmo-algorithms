import sys
sys.setrecursionlimit(1 << 20)

# n - число вершин
# edges - список ребер графа
# Возвращает число компонент связности и размер наибольшей из них
def components(n, edges) -> (int, int):
    graph = [[] for _ in range(n)]

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    used = [False] * n

    count = 0
    biggest = 0

    for start in range(n):
        if used[start]:
            continue

        count += 1
        size = 0

        stack = [start]
        used[start] = True

        while stack:
            versh = stack.pop()
            size += 1

            for neighbor in graph[versh]:
                if not used[neighbor]:
                    used[neighbor] = True
                    stack.append(neighbor)

        biggest = max(biggest, size)

    return count, biggest