"""
Семинар — иные деревья поиска (тема 7).

Три независимые задачи (без импортов между ними). Условия — в README.md.
Проверка:

    python -m pytest 7_other_search_tree/seminar/seminar_tasks.py -q

Эталонные решения — в блоке REFERENCE SOLUTION внизу (закомментированы).
"""

from __future__ import annotations

# =============================================================================
# Задача 1 — B-дерево: вставки и поиски
# =============================================================================
#
# Положительное x  → вставить x в B-дерево с параметром t
# Отрицательное x  → найти abs(x), добавить True/False в ответ
# Вернуть только результаты поисков, по порядку.
# Используйте BTreeNode ниже.
#
# Пример:
#   process_btree_ops([1, 2, 3, 4, 5, -3, -9], t=3) -> [True, False]


class BTreeNode:
    """Узел B-дерева: ключи по возрастанию, children[i] — поддерево между ключами."""

    def __init__(self, leaf: bool = True) -> None:
        self.leaf = leaf
        self.keys: list[int] = []
        self.children: list[BTreeNode] = []


def process_btree_ops(ops: list[int], t: int = 3) -> list[bool]:
    raise NotImplementedError


# =============================================================================
# Задача 2 — вставка в красно-чёрное дерево
# =============================================================================
#
# Вставить key красным листом (правило BST), затем починить цвета/повороты.
# Вернуть корень (всегда чёрный). Дубликат: дерево не менять.
# Используйте RBNode; повороты rb_rotate_left / rb_rotate_right уже реализованы.
#
# Пример:
#   root = None
#   for key in [7, 3, 18, 10]:
#       root = rb_insert(root, key)
#   # root.color == "B"; нет двух красных подряд на ребре родитель–ребёнок


class RBNode:
    """Узел красно-чёрного дерева: key, color ("R"|"B"), left/right/parent."""

    def __init__(
        self,
        key: int,
        color: str = "R",
        left: RBNode | None = None,
        right: RBNode | None = None,
        parent: RBNode | None = None,
    ) -> None:
        self.key = key
        self.color = color  # "R" | "B"
        self.left = left
        self.right = right
        self.parent = parent


def rb_rotate_left(root: RBNode, x: RBNode) -> RBNode:
    y = x.right
    assert y is not None
    x.right = y.left
    if y.left is not None:
        y.left.parent = x
    y.parent = x.parent
    if x.parent is None:
        root = y
    elif x is x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y
    y.left = x
    x.parent = y
    return root


def rb_rotate_right(root: RBNode, y: RBNode) -> RBNode:
    x = y.left
    assert x is not None
    y.left = x.right
    if x.right is not None:
        x.right.parent = y
    x.parent = y.parent
    if y.parent is None:
        root = x
    elif y is y.parent.left:
        y.parent.left = x
    else:
        y.parent.right = x
    x.right = y
    y.parent = x
    return root


def rb_insert(root: RBNode | None, key: int) -> RBNode:
    raise NotImplementedError


# =============================================================================
# Задача 3 — автодополнение: top-K по префиксу
# =============================================================================
#
# Построить Trie по words. top_k(prefix, k) — не больше k слов с этим префиксом.
# Порядок ответа = порядок появления в words (не лексикографический).
# Пустой prefix: все слова, всё равно не больше k. k == 0 или нет совпадений → [].
# Используйте TrieNode ниже.
#
# Пример:
#   ac = Autocomplete(["бег", "бегать", "беговой", "бегство", "лес"])
#   ac.top_k("бег", 3) -> ["бег", "бегать", "беговой"]


class TrieNode:
    """Узел префиксного дерева: рёбра по символу, is_word — конец слова."""

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word: bool = False


class Autocomplete:
    def __init__(self, words: list[str]) -> None:
        raise NotImplementedError

    def top_k(self, prefix: str, k: int) -> list[str]:
        raise NotImplementedError


# =============================================================================
# Тесты
# =============================================================================


def test_btree_ops_basic():
    assert process_btree_ops([1, 2, 3, 4, 5, -3, -9], t=3) == [True, False]


def test_btree_ops_overflow_and_order():
    ops = [10, 20, 5, 6, 12, 30, 7, 17, -12, -7, -99, 3, -3]
    assert process_btree_ops(ops, t=3) == [True, True, False, True]


def test_btree_ops_empty_searches():
    assert process_btree_ops([-1, -2], t=3) == [False, False]


def _rb_no_rr(node: RBNode | None) -> bool:
    if node is None:
        return True
    if node.color == "R":
        for ch in (node.left, node.right):
            if ch is not None and ch.color == "R":
                return False
    return _rb_no_rr(node.left) and _rb_no_rr(node.right)


def _rb_black_height(node: RBNode | None) -> int | None:
    if node is None:
        return 0
    left = _rb_black_height(node.left)
    right = _rb_black_height(node.right)
    if left is None or right is None or left != right:
        return None
    return left + (1 if node.color == "B" else 0)


def test_rb_insert_root_black_and_rules():
    root = None
    for key in [7, 3, 18, 10, 22, 8, 11, 26]:
        root = rb_insert(root, key)
    assert root is not None
    assert root.color == "B"
    assert _rb_no_rr(root)
    assert _rb_black_height(root) is not None


def test_rb_insert_line_case():
    root = None
    for key in [10, 20, 30]:
        root = rb_insert(root, key)
    assert root is not None
    assert root.key == 20
    assert root.color == "B"
    assert root.left is not None and root.right is not None
    assert root.left.key == 10 and root.right.key == 30


def test_rb_insert_duplicate_noop():
    root = rb_insert(None, 5)
    root2 = rb_insert(root, 5)
    assert root2 is root
    assert root2.left is None and root2.right is None


def test_autocomplete_top_k():
    words = ["бег", "бегать", "беговой", "бегство", "лес", "беглец"]
    ac = Autocomplete(words)
    assert ac.top_k("бег", 3) == ["бег", "бегать", "беговой"]
    assert ac.top_k("лес", 5) == ["лес"]
    assert ac.top_k("xyz", 3) == []
    assert ac.top_k("бег", 0) == []


def test_autocomplete_empty_prefix():
    ac = Autocomplete(["а", "б", "в"])
    assert ac.top_k("", 2) == ["а", "б"]


# =============================================================================
# REFERENCE SOLUTION (for staff; keep commented for students)
# =============================================================================
#
# def process_btree_ops(ops: list[int], t: int = 3) -> list[bool]:
#     root = BTreeNode(True)
#     results: list[bool] = []
#
#     def split_child(parent: BTreeNode, i: int) -> None:
#         y = parent.children[i]
#         z = BTreeNode(y.leaf)
#         mid = y.keys[t - 1]
#         z.keys = y.keys[t:]
#         y.keys = y.keys[: t - 1]
#         if not y.leaf:
#             z.children = y.children[t:]
#             y.children = y.children[:t]
#         parent.children.insert(i + 1, z)
#         parent.keys.insert(i, mid)
#
#     def insert_nonfull(node: BTreeNode, key: int) -> None:
#         i = len(node.keys) - 1
#         if node.leaf:
#             node.keys.append(0)
#             while i >= 0 and key < node.keys[i]:
#                 node.keys[i + 1] = node.keys[i]
#                 i -= 1
#             node.keys[i + 1] = key
#             return
#         while i >= 0 and key < node.keys[i]:
#             i -= 1
#         i += 1
#         if len(node.children[i].keys) == 2 * t - 1:
#             split_child(node, i)
#             if key > node.keys[i]:
#                 i += 1
#         insert_nonfull(node.children[i], key)
#
#     def insert(key: int) -> None:
#         nonlocal root
#         if len(root.keys) == 2 * t - 1:
#             new_root = BTreeNode(False)
#             new_root.children = [root]
#             root = new_root
#             split_child(new_root, 0)
#         insert_nonfull(root, key)
#
#     def search(key: int) -> bool:
#         node = root
#         while True:
#             i = 0
#             while i < len(node.keys) and key > node.keys[i]:
#                 i += 1
#             if i < len(node.keys) and node.keys[i] == key:
#                 return True
#             if node.leaf:
#                 return False
#             node = node.children[i]
#
#     for x in ops:
#         if x > 0:
#             insert(x)
#         elif x < 0:
#             results.append(search(abs(x)))
#     return results
#
#
# def rb_insert(root: RBNode | None, key: int) -> RBNode:
#     node = RBNode(key, "R")
#     if root is None:
#         node.color = "B"
#         return node
#     cur, parent = root, None
#     while cur is not None:
#         parent = cur
#         if key == cur.key:
#             return root
#         cur = cur.left if key < cur.key else cur.right
#     node.parent = parent
#     if key < parent.key:
#         parent.left = node
#     else:
#         parent.right = node
#
#     while node.parent is not None and node.parent.color == "R":
#         gp = node.parent.parent
#         if gp is None:
#             break
#         if node.parent is gp.left:
#             uncle = gp.right
#             if uncle is not None and uncle.color == "R":
#                 node.parent.color = "B"
#                 uncle.color = "B"
#                 gp.color = "R"
#                 node = gp
#             else:
#                 if node is node.parent.right:
#                     node = node.parent
#                     root = rb_rotate_left(root, node)
#                 node.parent.color = "B"
#                 gp.color = "R"
#                 root = rb_rotate_right(root, gp)
#         else:
#             uncle = gp.left
#             if uncle is not None and uncle.color == "R":
#                 node.parent.color = "B"
#                 uncle.color = "B"
#                 gp.color = "R"
#                 node = gp
#             else:
#                 if node is node.parent.left:
#                     node = node.parent
#                     root = rb_rotate_right(root, node)
#                 node.parent.color = "B"
#                 gp.color = "R"
#                 root = rb_rotate_left(root, gp)
#
#     while root.parent is not None:
#         root = root.parent
#     root.color = "B"
#     return root
#
#
# class Autocomplete:
#     def __init__(self, words: list[str]) -> None:
#         self._root = TrieNode()
#         self._order = list(words)
#         for w in words:
#             node = self._root
#             for ch in w:
#                 node = node.children.setdefault(ch, TrieNode())
#             node.is_word = True
#
#     def top_k(self, prefix: str, k: int) -> list[str]:
#         if k <= 0:
#             return []
#         node = self._root
#         for ch in prefix:
#             if ch not in node.children:
#                 return []
#             node = node.children[ch]
#         matched: list[str] = []
#
#         def dfs(n: TrieNode, path: str) -> None:
#             if n.is_word:
#                 matched.append(path)
#             for ch, child in n.children.items():
#                 dfs(child, path + ch)
#
#         dfs(node, prefix)
#         order_index = {w: i for i, w in enumerate(self._order)}
#         matched.sort(key=lambda w: order_index[w])
#         return matched[:k]