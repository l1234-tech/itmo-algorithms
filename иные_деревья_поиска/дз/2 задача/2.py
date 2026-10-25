import sys

RED = "R"
BLACK = "B"


class Node:
    __slots__ = ("key", "color", "left", "right", "parent")

    def __init__(self, key: int, color: str, parent=None) -> None:
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = parent


def is_red(node) -> bool:
    """Отсутствующая вершина (None) считается чёрной."""
    return node is not None and node.color == RED


class RedBlackTree:
    def __init__(self) -> None:
        self.root = None

    def find(self, key: int) -> bool:
        node = self.root
        while node is not None:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def _replace_child(self, parent, old, new) -> None:
        """Ставит new на место ребёнка old вершины parent (или на место корня)."""
        if parent is None:
            self.root = new
        elif parent.left is old:
            parent.left = new
        else:
            parent.right = new
        if new is not None:
            new.parent = parent

    def rotate_left(self, a) -> None:
        """Левый поворот вокруг a: правый ребёнок b встаёт на место a."""
        b = a.right
        a.right = b.left
        if b.left is not None:
            b.left.parent = a
        self._replace_child(a.parent, a, b)
        b.left = a
        a.parent = b

    def rotate_right(self, a) -> None:
        """Правый поворот вокруг a: левый ребёнок b встаёт на место a."""
        b = a.left
        a.left = b.right
        if b.right is not None:
            b.right.parent = a
        self._replace_child(a.parent, a, b)
        b.right = a
        a.parent = b

    def preorder(self) -> list:
        """Вершины в порядке прямого обхода в виде строк "<ключ><цвет>"."""
        result = []
        stack = [self.root] if self.root is not None else []
        while stack:
            node = stack.pop()
            result.append(f"{node.key}{node.color}")
            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)
        return result

    def insert(self, key: int) -> None:
        """Вставляет ключ по правилам из условия; если ключ уже есть, ничего не делает."""

        if self.root is None:
            return Node(key)

        if not self.find(key):
            return 

        if key < self.root.key:
            self.root = self.root
            self.root.left = self.insert(key)
        
        raise NotImplementedError

    def fix_insert(self, z) -> None:
        """Восстанавливает свойства красно-чёрного дерева после добавления красной вершины z."""
        # TODO
        raise NotImplementedError


def main() -> None:
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    pos = 1
    tree = RedBlackTree()
    out = []

    for _ in range(q):
        cmd = data[pos]
        if cmd == b"add":
            tree.insert(int(data[pos + 1]))
            pos += 2
        elif cmd == b"exists":
            out.append("YES" if tree.find(int(data[pos + 1])) else "NO")
            pos += 2
        elif cmd == b"root":
            out.append(str(tree.root.key) if tree.root is not None else "Empty")
            pos += 1
        else:  # print
            out.append(" ".join(tree.preorder()) if tree.root is not None else "Empty")
            pos += 1

    sys.stdout.write("".join(line + "\n" for line in out))


if __name__ == "__main__":
    main()