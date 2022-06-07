import heapq as hq

def get_weight(i, j): # get w ( edge : i -> j) [ directed ]
    if i < n and j < n:
        return 2*w[i][j]
    i %= n
    j %= n
    return w[i][j]

def is_thief_extended(i):
    if i >= n:
        return False
    return is_thief[i]
    

def closest_thief_without_car(g):
    d = [(0, g)]
    table =[10**15 for _ in range(n)]
    table[g] = 0

    ret = {}

    while len(d) != 0:
        temp = hq.heappop(d)
        if is_thief[temp[1]]:
            return temp[0]
        if temp[1] in ret or has_car[i]:
            continue
        ret[temp[1]] = temp[0]
        for j in adj[temp[1]]:
            if temp[0] + w[temp[1]][j] < table[j]:
                hq.heappush(d, (temp[0] + w[temp[1]][j], j))
                table[j] = temp[0] + w[temp[1]][j]
    return 10**20

def tin_tin_shortest_path(s, g):
    d = [(0, s)]
    table =[10**15 for _ in range(n)]
    table[s] = 0

    ret = {}
    path = [-1] * n

    while len(d) != 0:
        temp = hq.heappop(d)
        if temp[1] == g:
            return temp[0], path
        if temp[1] in ret:
            continue
        ret[temp[1]] = temp[0]
        for j in adj[temp[1]]:
            if temp[0] + w[temp[1]][j] < table[j]:
                hq.heappush(d, (temp[0] + w[temp[1]][j], j))
                path[j] = temp[1]
                table[j] = temp[0] + w[temp[1]][j]
    return 10**20


def closest_thief_to_g(g): # start from g , find closest thief
    d = [(0, g)]
    table =[10**15 for _ in range(2*n)]
    done = [False] * (2*n)
    table[g] = 0

    while len(d) != 0:
        temp = hq.heappop(d)
        if is_thief_extended(temp[1]):
            return temp[0]
        if done[temp[1]]:
            continue
        done[temp[1]] = True
        if temp[1] >= n:
            for j in adj[temp[1] - n]:
                if temp[0] + get_weight(temp[1], j + n) < table[j + n]:
                    hq.heappush(d, (temp[0] + get_weight(temp[1], j + n), j + n))
                    table[j + n] = temp[0] + get_weight(temp[1], j + n)
            for j in adj_temp[temp[1] - n]:
                if temp[0] + get_weight(temp[1], j) < table[j]:
                    hq.heappush(d, (temp[0] + get_weight(temp[1], j), j))
                    table[j] = temp[0] + get_weight(temp[1], j)
        else:
            for j in adj[temp[1]]:
                if temp[0] + get_weight(temp[1], j) < table[j]:
                    hq.heappush(d, (temp[0] + get_weight(temp[1], j), j))
                    table[j] = temp[0] + get_weight(temp[1], j)
    return 10**20

k = int(input())

for _ in range(k):
    n, m = map(int, input().split())

    adj = [[] for _ in range(n)]
    w = [{} for _ in range(n)]

    has_car = [False] * n
    is_thief = [False] * n

    for i in range(m):
        u, v, d = map(int, input().split())
        u -= 1
        v -= 1
        adj[v].append(u)
        adj[u].append(v)

        w[u][v] = d
        w[v][u] = d

    t = int(input())

    dozd_locs = [int(i) - 1 for i in input().split()]
    
    c = int(input())
    car_locs = [int(i) - 1 for i in input().split()]

    for i in car_locs:
        has_car[i] = True

    for i in dozd_locs:
        is_thief[i] = True

    s, g = map(int, input().split())
    s -= 1
    g -= 1

    tintin_dist, tintin_path = tin_tin_shortest_path(s, g)

    shortest1 = closest_thief_without_car(g)
    if shortest1 < tintin_dist:
        print('Poor Tintin')
        continue

    # create new graph :


    adj_temp = [[] for _ in range(n)]
    for i in car_locs:
        for j in adj[i]:
            adj_temp[j].append(i)

    

    # new graph created

    
    shortest2 = closest_thief_to_g(g + n)

    if shortest2 < tintin_dist*2:
        print('Poor Tintin')
    else:
        print(tintin_dist)

        shahrs_num = 0
        shahrs = ''
        while g != -1:
            shahrs_num += 1
            shahrs = f'{g + 1} ' + shahrs
            g = tintin_path[g]
        print(shahrs_num)
        print(shahrs)