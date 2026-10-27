"""
Семинар — хеш-таблицы (тема 8).

Три независимые задачи (без импортов между ними). Условия — в README.md.
Проверка:

    python -m pytest 8_hash_tables/seminar/seminar_tasks.py -q

Эталонные решения — в блоке REFERENCE SOLUTION внизу (закомментированы).
Для локальной проверки эталона раскомментируйте REFERENCE и закомментируйте stubs.
"""

from __future__ import annotations

from collections.abc import Callable

# =============================================================================
# Задача 1 — OpenHashMap: открытая адресация (линейный пробинг)
# =============================================================================
#
# Ключи: целые от 1 до 10^8 (это область ключей, не размер таблицы).
# Запрещены dict и set.
#
# Контракт, который проверяют тесты:
#   - self.capacity — ёмкость таблицы (задаётся в конструкторе)
#   - self.slots — список длины capacity
#   - пустой слот: None
#   - занятый слот: пара (key, value)
#   - удалённый слот: объект TOMBSTONE (уже определён ниже)
#   - h(key) = key % capacity  (метод _index)
#   - при коллизии: линейный пробинг (h + 1, h + 2, ...) % capacity
#
# API: put(key, value), get(key) -> value | None, remove(key) -> bool
#
# Пример (capacity=7):
#   m = OpenHashMap(7)
#   m.put(1, "a"); m.put(8, "b"); m.put(15, "c")
#   # слоты: index 1 → (1,"a"), 2 → (8,"b"), 3 → (15,"c")


TOMBSTONE = object()


class OpenHashMap:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.slots: list = [None] * capacity
        self.size = 0

    def _index(self, key: int) -> int:
        return key % self.capacity

    def put(self, key: int, value: object) -> None:
        raise NotImplementedError

    def get(self, key: int) -> object | None:
        raise NotImplementedError

    def remove(self, key: int) -> bool:
        raise NotImplementedError


# =============================================================================
# Задача 2 — LRUCache
# =============================================================================
#
# Кэш фиксированной ёмкости capacity.
# get(key) → value или None; при попадании ключ становится самым «свежим».
# put(key, value): обновить или вставить; при переполнении вытеснить
# самый давно не использованный (Least Recently Used).
#
# Запрещены dict и set. Списки / своя хеш-таблица — можно.
# O(n) поиск по списку допустим: важна политика LRU.
#
# Пример:
#   c = LRUCache(2)
#   c.put(1, 1); c.put(2, 2)
#   c.get(1) -> 1
#   c.put(3, 3)   # вытеснен ключ 2
#   c.get(2) -> None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        raise NotImplementedError

    def get(self, key: int) -> object | None:
        raise NotImplementedError

    def put(self, key: int, value: object) -> None:
        raise NotImplementedError


# =============================================================================
# Задача 3 — MRUCache с TTL (Most Frequently Used по смыслу пары)
# =============================================================================
#
# У каждой записи счётчик обращений (частота): +1 при каждом успешном get
# и при put (вставка или обновление).
# При переполнении вытесняется ключ с **наибольшей** частотой
# (самый часто используемый). При равенстве частот — любой из них
# (эталон и тесты: первый с максимальной частотой в списке).
#
# TTL: срок жизни ttl секунд с момента put/обновления.
# get просроченной → None. Просроченные не считаются живыми.
#
# now: Callable[[], float] — часы для тестов (не вызывайте time.time()).
# Запрещены dict и set.
#
# Пример:
#   t = [0.0]
#   c = MRUCache(2, ttl=5.0, now=lambda: t[0])
#   c.put(1, "a"); c.put(2, "b")   # частоты 1 и 1
#   c.get(1); c.get(1)             # частота 1 → 3
#   c.put(3, "c")                  # вытеснен 1 (чаще всех)
#   c.get(1) -> None
#   t[0] = 10.0
#   c.get(2) -> None               # TTL истёк


class MRUCache:
    def __init__(
        self,
        capacity: int,
        ttl: float,
        now: Callable[[], float],
    ) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        raise NotImplementedError

    def get(self, key: int) -> object | None:
        raise NotImplementedError

    def put(self, key: int, value: object) -> None:
        raise NotImplementedError


# =============================================================================
# Тесты
# =============================================================================


def test_open_hash_map_basic_put_get():
    m = OpenHashMap(8)
    m.put(1, "one")
    m.put(2, "two")
    assert m.get(1) == "one"
    assert m.get(2) == "two"
    assert m.get(3) is None


def test_open_hash_map_linear_probing_layout():
    """Коллизии 1, 8, 15 при capacity=7 → слоты 1, 2, 3 (не цепочка в одном слоте)."""
    m = OpenHashMap(7)
    m.put(1, "a")
    m.put(8, "b")
    m.put(15, "c")
    assert m.slots[1] == (1, "a")
    assert m.slots[2] == (8, "b")
    assert m.slots[3] == (15, "c")
    # слот-корзина не должен быть списком (цепочки)
    assert not isinstance(m.slots[1], list)
    assert m.get(15) == "c"


def test_open_hash_map_update_and_remove_with_tombstone():
    m = OpenHashMap(7)
    m.put(1, "a")
    m.put(8, "b")
    m.put(1, "A")
    assert m.get(1) == "A"
    assert m.remove(1) is True
    assert m.slots[1] is TOMBSTONE
    assert m.get(8) == "b"  # поиск проходит через надгробие
    assert m.get(1) is None
    m.put(15, "c")  # может занять надгробие или следующий свободный
    assert m.get(15) == "c"
    assert m.get(8) == "b"


def test_open_hash_map_large_keys():
    m = OpenHashMap(11)
    keys = [1, 10**8, 10**8 - 1, 42]
    for k in keys:
        m.put(k, k * 2)
    for k in keys:
        assert m.get(k) == k * 2


def test_lru_cache_leetcode_style():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) is None
    c.put(4, 4)
    assert c.get(1) is None
    assert c.get(3) == 3
    assert c.get(4) == 4


def test_lru_cache_update_refreshes():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)  # 1 стал свежим
    c.put(3, 3)  # вытеснен 2
    assert c.get(1) == 10
    assert c.get(2) is None
    assert c.get(3) == 3


def test_mru_cache_evicts_most_frequent():
    t = [0.0]
    c = MRUCache(2, ttl=100.0, now=lambda: t[0])
    c.put(1, "a")
    c.put(2, "b")
    assert c.get(1) == "a"
    assert c.get(1) == "a"  # частота ключа 1 выше
    c.put(3, "c")  # вытесняется 1 (самый частый)
    assert c.get(1) is None
    assert c.get(2) == "b"
    assert c.get(3) == "c"


def test_mru_cache_ttl_expires():
    t = [0.0]
    c = MRUCache(2, ttl=5.0, now=lambda: t[0])
    c.put(1, "a")
    c.put(2, "b")
    t[0] = 6.0
    assert c.get(1) is None
    assert c.get(2) is None
    c.put(3, "c")
    assert c.get(3) == "c"


def test_mru_expired_not_counted_toward_capacity():
    t = [0.0]
    c = MRUCache(2, ttl=5.0, now=lambda: t[0])
    c.put(1, "a")
    c.put(2, "b")
    t[0] = 6.0  # обе просрочены
    c.put(3, "c")
    c.put(4, "d")  # не должно вытеснять «живые» — их нет
    assert c.get(3) == "c"
    assert c.get(4) == "d"


# =============================================================================
# REFERENCE SOLUTION (for staff; keep commented for students)
# =============================================================================
#
# class OpenHashMap:
#     def __init__(self, capacity: int) -> None:
#         if capacity <= 0:
#             raise ValueError("capacity must be positive")
#         self.capacity = capacity
#         self.slots: list = [None] * capacity
#         self.size = 0
#
#     def _index(self, key: int) -> int:
#         return key % self.capacity
#
#     def put(self, key: int, value: object) -> None:
#         first_tomb = None
#         for j in range(self.capacity):
#             i = (self._index(key) + j) % self.capacity
#             cell = self.slots[i]
#             if cell is None:
#                 dest = first_tomb if first_tomb is not None else i
#                 if self.slots[dest] is not TOMBSTONE and self.slots[dest] is None:
#                     self.size += 1
#                 elif self.slots[dest] is TOMBSTONE:
#                     self.size += 1
#                 self.slots[dest] = (key, value)
#                 return
#             if cell is TOMBSTONE:
#                 if first_tomb is None:
#                     first_tomb = i
#                 continue
#             k, _ = cell
#             if k == key:
#                 self.slots[i] = (key, value)
#                 return
#         raise RuntimeError("table is full")
#
#     def get(self, key: int) -> object | None:
#         for j in range(self.capacity):
#             i = (self._index(key) + j) % self.capacity
#             cell = self.slots[i]
#             if cell is None:
#                 return None
#             if cell is TOMBSTONE:
#                 continue
#             k, v = cell
#             if k == key:
#                 return v
#         return None
#
#     def remove(self, key: int) -> bool:
#         for j in range(self.capacity):
#             i = (self._index(key) + j) % self.capacity
#             cell = self.slots[i]
#             if cell is None:
#                 return False
#             if cell is TOMBSTONE:
#                 continue
#             k, _ = cell
#             if k == key:
#                 self.slots[i] = TOMBSTONE
#                 self.size -= 1
#                 return True
#         return False
#
#
# class LRUCache:
#     def __init__(self, capacity: int) -> None:
#         if capacity <= 0:
#             raise ValueError("capacity must be positive")
#         self.capacity = capacity
#         # список пар [key, value]; индекс 0 — самый старый, -1 — самый свежий
#         self._items: list[list] = []
#
#     def _find(self, key: int) -> int:
#         for i, (k, _) in enumerate(self._items):
#             if k == key:
#                 return i
#         return -1
#
#     def get(self, key: int) -> object | None:
#         i = self._find(key)
#         if i < 0:
#             return None
#         item = self._items.pop(i)
#         self._items.append(item)
#         return item[1]
#
#     def put(self, key: int, value: object) -> None:
#         i = self._find(key)
#         if i >= 0:
#             self._items.pop(i)
#         elif len(self._items) >= self.capacity:
#             self._items.pop(0)
#         self._items.append([key, value])
#
#
# class MRUCache:
#     def __init__(
#         self,
#         capacity: int,
#         ttl: float,
#         now: Callable[[], float],
#     ) -> None:
#         if capacity <= 0:
#             raise ValueError("capacity must be positive")
#         if ttl <= 0:
#             raise ValueError("ttl must be positive")
#         self.capacity = capacity
#         self.ttl = ttl
#         self._now = now
#         # [key, value, expire_at, freq]
#         self._items: list[list] = []
#
#     def _purge_expired(self) -> None:
#         now = self._now()
#         self._items = [it for it in self._items if it[2] > now]
#
#     def _find(self, key: int) -> int:
#         for i, (k, _, _, _) in enumerate(self._items):
#             if k == key:
#                 return i
#         return -1
#
#     def _evict_most_frequent(self) -> None:
#         best_i = 0
#         best_f = self._items[0][3]
#         for i in range(1, len(self._items)):
#             if self._items[i][3] > best_f:
#                 best_f = self._items[i][3]
#                 best_i = i
#         self._items.pop(best_i)
#
#     def get(self, key: int) -> object | None:
#         self._purge_expired()
#         i = self._find(key)
#         if i < 0:
#             return None
#         self._items[i][3] += 1
#         return self._items[i][1]
#
#     def put(self, key: int, value: object) -> None:
#         self._purge_expired()
#         i = self._find(key)
#         expire = self._now() + self.ttl
#         if i >= 0:
#             self._items[i][1] = value
#             self._items[i][2] = expire
#             self._items[i][3] += 1
#             return
#         if len(self._items) >= self.capacity:
#             self._evict_most_frequent()
#         self._items.append([key, value, expire, 1])
