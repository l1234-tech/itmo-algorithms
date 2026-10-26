f = open('хеш таблицы/дз/3 задача/input.txt')

n , s = map(int , f.readline().split())

balance = [int(x) for x in f.readline().split()]

prefix_sum = {0 : 1}

P = 0
answer = 0

for i in range(len(balance)):
    P += balance[i]

    answer += prefix_sum.get(P - s, 0)

    prefix_sum[P] = prefix_sum.get(P, 0) + 1

print(answer)