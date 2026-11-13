import sys
from collections import deque

f = open("базовые алгоритмы на графы/дз/2 задача/input.txt", "r")
h, w = map(int, f.readline().split())

grid = []
start = None
target = None

for i in range(h):
    row = f.readline().strip()
    grid.append(row)

    for j in range(w):
        if row[j] == 'S':
            start = (i, j)
        elif row[j] == 'T':
            target = (i, j)

dist = [[-1] * w for _ in range(h)]

queue = deque([start])

start_row, start_col = start
dist[start_row][start_col] = 0

while queue:
    row , col = queue.popleft()

    if (row, col) == target:
        break

    if row > 0 and grid[row - 1][col] != '#' and dist[row - 1][col] == -1:
        dist[row - 1][col] = dist[row][col] + 1
        queue.append((row - 1, col))

    if row + 1 < h and grid[row + 1][col] != '#' and dist[row + 1][col] == -1:
        dist[row + 1][col] = dist[row][col] + 1
        queue.append((row + 1, col))

    if col > 0 and grid[row][col - 1] != '#' and dist[row][col - 1] == -1:
        dist[row][col - 1] = dist[row][col] + 1
        queue.append((row, col - 1))

    if col + 1 < w and grid[row][col + 1] != '#' and dist[row][col + 1] == -1:
        dist[row][col + 1] = dist[row][col] + 1
        queue.append((row, col + 1))

target_row , target_col = target 
print(dist[target_row][target_col])