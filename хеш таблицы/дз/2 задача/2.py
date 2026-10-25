f = open('хеш таблицы/дз/2 задача/input.txt')

n, k = map(int , f.readline().split())

queue = [int(x) for x in f.readline().split()]

hash_dict = {}

for i in range(k):
    number = queue[i]
    hash_dict[number] = hash_dict.get(number, 0) + 1

buff = [len(hash_dict)]

for i in range(k, n):
    out = [queue[i - k]]
    hash_dict[out[0]] -= 1

    if hash_dict[out[0]] == 0:
        del hash_dict[out[0]]

    inc = queue[i]
    hash_dict[inc] = hash_dict.get(inc, 0) + 1
    buff.append(len(hash_dict))

result = [str(x) for x in buff]

print(*result)