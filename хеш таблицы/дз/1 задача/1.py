f = open('хеш таблицы/дз/1 задача/input.txt')

n = int(f.readline())

hash_dict = {}

def hash_rule(word):
    return "".join(sorted(word))

def add_hash(word, hash_dict):
    if hash_dict.get(hash_rule(word)) is None:
        hash_dict[hash_rule(word)] = 1
        return

    else:
        new_value = hash_dict[hash_rule(word)] + 1
        hash_dict[hash_rule(word)] = new_value
        return 


for _ in range(n):
    word = f.readline()
    add_hash(word, hash_dict)

print(len(hash_dict) , max(hash_dict.values()))