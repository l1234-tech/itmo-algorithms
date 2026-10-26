class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self):
        self.capacity = 10
        self.size = 0
        self.buckets = [None] * self.capacity

    def polinominal_hash(self, s: str, p: int = 257, m: int = 10**9 + 7) -> int:
        hash_value = 0
        for char in s:
            hash_value = (hash_value * p + ord(char)) % m

        return hash_value

    def check_capasity(self) -> bool:
        return (self.size / self.capacity) <= 1

    def increase_capasity(self):
        old_buckets = self.buckets

        self.capacity *= 2
        self.buckets = [None] * self.capacity

        for item in old_buckets:
            curr_item = item

            while curr_item is not None:
                next_item = curr_item.next
                index = (self.polinominal_hash(curr_item.key) % self.capacity)
                curr_item.next = self.buckets[index]
                self.buckets[index] = curr_item
                curr_item = next_item

    def put(self, key: str, value: int) -> None:
        index = self.polinominal_hash(key) % self.capacity
        curr_item = self.buckets[index]

        while curr_item is not None:
            if curr_item.key == key:
                curr_item.value = value
                return

            curr_item = curr_item.next

        new_item = Node(key, value)
        new_item.next = self.buckets[index]
        self.buckets[index] = new_item
        self.size += 1

        if not self.check_capasity():
            self.increase_capasity()

    def get(self, key: str):
        index = self.polinominal_hash(key) % self.capacity
        curr_item = self.buckets[index]

        while curr_item is not None:
            if curr_item.key == key:
                return curr_item.value

            curr_item = curr_item.next

        return "Error"

    def delete(self, key: str):
        index = self.polinominal_hash(key) % self.capacity
        curr_item = self.buckets[index]

        prev_item = None

        while curr_item is not None:
            if curr_item.key == key:
                if prev_item is None:
                    self.buckets[index] = curr_item.next
                else:
                    prev_item.next = curr_item.next

                self.size -= 1
                return curr_item.value

            prev_item = curr_item
            curr_item = curr_item.next

        return "Error"

    def table_size(self):
        return self.size


def main():
    with open("input.txt", encoding="utf-8") as f:
        n = int(f.readline())
        Hash_Table = HashTable()

        for _ in range(n):
            buff = f.readline().split()

            if len(buff) == 3:
                key = buff[1]
                value = int(buff[2])
                Hash_Table.put(key, value)

            elif len(buff) == 1:
                print(Hash_Table.table_size())

            else:
                cmd = buff[0]
                key = buff[1]

                if cmd == "get":
                    print(Hash_Table.get(key))
                else:
                    print(Hash_Table.delete(key))


if __name__ == "__main__":
    main()