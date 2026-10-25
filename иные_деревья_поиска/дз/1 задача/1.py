from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class RBNode:
    key: int
    color: str  # "R" | "B"
    left: Optional["RBNode"] = None
    right: Optional["RBNode"] = None
    parent: Optional["RBNode"] = None

def dfs(node: RBNode | None, min_key: int | None,  max_key: int | None) -> int | None:
    if node is None:
        return 1

    if node.color not in ("R", "B"):
        return None

    if min_key is not None and node.key <= min_key:
        return None

    if max_key is not None and node.key >= max_key:
        return None

    if node.color == "R":
        if node.left is not None and node.left.color == "R":
            return None
        if node.right is not None and node.right.color == "R":
            return None
    
    lh = dfs(node.left, min_key, node.key)
    rh = dfs(node.right, node.key, max_key)
    if lh is None or rh is None or lh != rh:
        return None
    return lh + (1 if node.color == "B" else 0)

def check_rb_tree(root: RBNode | None):
    if root is not None and root.color != "B":
        return False, 0

    black_height = dfs(root, None, None)

    if black_height is None:
        return False, 0

    return True, black_height

f = open("иные_деревья_поиска/дз/1 задача/input.txt")

n = int(f.readline())

nodes = [None] * (n + 1)

children = []

for i in range(1, n + 1):
    key , color , left , right = f.readline().split()
    nodes[i] = RBNode(int(key) , color)
    children.append((int(left), int(right)))

for i in range(1, n + 1):

    left , right = children[i - 1]

    if left != 0:
        nodes[i].left = nodes[left]
        nodes[left].parent = nodes[i]

    if right != 0:
        nodes[i].right = nodes[right]
        nodes[right].parent = nodes[i]

root = nodes[1]

is_rb_tree, black_height = check_rb_tree(root)

if is_rb_tree is True:
    print("YES", black_height - 1)
else:
    print("NO")