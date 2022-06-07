import heapq as hq

def state_to_number(arr):
    s = 0
    p = 1
    for i in range(n):
        for j in range(m):
            s += arr[i][j]*p
            p *= 13
    return s

def number_to_state(num):
    ret = []
    ret2 = [False]*(m*n)
    num_done = 0
    temp = sum_mins
    for i in range(n):
        ret.append([])
        for _ in range(m):
            ret[i].append(num % 13)
            if num % 13 < n*m:
                num_done += 1
                ret2[num%13] = True
                temp -= mins[num%13]
            num = num // 13
    return ret, ret2, num_done, temp


n, m = map(int, input().split())
all_tiles = []
mins = []
ls = {}
rs = {}
us = {}
ds = {}

for i in range(m*n):
    u, r, d, l = map(int, input().split())
    all_tiles.append((u, r, d, l))

    mins.append(min(min(min(u, r), l), d))

    if l in ls:
        ls[l].append(i)
    else:
        ls[l] = [i]
    
    if d in ds:
        ds[d].append(i)
    else:
        ds[d] = [i]

    if u in us:
        us[u].append(i)
    else:
        us[u] = [i]

    if r in rs:
        rs[r].append(i)
    else:
        rs[r] = [i]

sum_mins = sum(mins)

h = []
board = [[12] * m for _ in range(n)]
board[0][0] = 0
temp = state_to_number(board)

seen = {}
min_cost = 10**20
for i in range(n*m):
    sum_mins -= mins[i]
    hq.heappush(h, (sum_mins, temp + i))
    sum_mins += mins[i]

while h:
    cost, number = hq.heappop(h)
    if number in seen:
        continue
    seen[number] = True
    board, tile_exists, num_done, heu = number_to_state(number)
    # print(f'{board} -> {cost - heu} -> {heu}')
    if num_done == m*n:
        print(cost)
        exit(0)
    
    for i in range(n):
        for j in range(m):
            if board[i][j] != 12:
                continue
            

            options = set()
            if i == 0:
                if board[i + 1][j] != 12:
                    if all_tiles[board[i + 1][j]][0] in ds:
                        for k in ds[all_tiles[board[i + 1][j]][0]]:
                            if tile_exists[k]:
                                continue
                            # board[i][j] = k
                            # heu -= mins[k]
                            if cost + all_tiles[k][2] - mins[k] < min_cost:
                                # hq.heappush(h, (cost + all_tiles[k][2] - mins[k], state_to_number(board)))
                                options.add((k, 2))
                            # heu += mins[k]
            elif i == n - 1:
                if board[i - 1][j] != 12:
                    if all_tiles[board[i - 1][j]][2] in us:
                        for k in us[all_tiles[board[i - 1][j]][2]]:
                            if tile_exists[k]:
                                continue
                            # board[i][j] = k
                            # heu -= mins[k]
                            if cost + all_tiles[k][0] - mins[k] < min_cost:
                                # hq.heappush(h, (cost + all_tiles[k][0] - mins[k], state_to_number(board)))
                                options.add((k, 0))
                            # heu += mins[k]
            else:
                if board[i - 1][j] != 12:
                    if all_tiles[board[i - 1][j]][2] in us:
                        for k in us[all_tiles[board[i - 1][j]][2]]:
                            if tile_exists[k]:
                                continue
                            # board[i][j] = k
                            # heu -= mins[k]
                            if cost + all_tiles[k][0] - mins[k] < min_cost:
                                # hq.heappush(h, (cost + all_tiles[k][0] - mins[k], state_to_number(board)))
                                options.add((k, 0))
                            # heu += mins[k]
                if board[i + 1][j] != 12:
                    if all_tiles[board[i + 1][j]][0] in ds:
                        for k in ds[all_tiles[board[i + 1][j]][0]]:
                            if tile_exists[k]:
                                continue
                            # board[i][j] = k
                            # heu -= mins[k]
                            if cost + all_tiles[k][2] - mins[k] < min_cost:
                                # hq.heappush(h, (cost + all_tiles[k][2] - mins[k], state_to_number(board)))
                                options.add((k, 2))
                            # heu += mins[k]

            if j == 0:
                if board[i][j + 1] != 12:
                    if all_tiles[board[i][j + 1]][3] in rs:
                        for k in rs[all_tiles[board[i][j + 1]][3]]:
                            if tile_exists[k]:
                                continue
                            # board[i][j] = k
                            # heu -= mins[k]
                            if cost + all_tiles[k][1] - mins[k] < min_cost:
                                # hq.heappush(h, (cost + all_tiles[k][1] - mins[k], state_to_number(board)))
                                options.add((k, 1))
                            # heu += mins[k]
            elif j == m - 1:
                if board[i][j - 1] != 12:
                    if all_tiles[board[i][j - 1]][1] in ls:
                        for k in ls[all_tiles[board[i][j - 1]][1]]:
                            if tile_exists[k]:
                                continue
                            # board[i][j] = k
                            # heu -= mins[k]
                            if cost + all_tiles[k][3] - mins[k] < min_cost:
                                # hq.heappush(h, (cost + all_tiles[k][3] - mins[k], state_to_number(board)))
                                options.add((k, 3))
                            # heu += mins[k]
            else:
                if board[i][j - 1] != 12:
                    if all_tiles[board[i][j - 1]][1] in ls:
                        for k in ls[all_tiles[board[i][j - 1]][1]]:
                            if tile_exists[k]:
                                continue
                            # board[i][j] = k
                            # heu -= mins[k]
                            if cost + all_tiles[k][3] - mins[k] < min_cost:
                                # hq.heappush(h, (cost + all_tiles[k][3] - mins[k], state_to_number(board)))
                                options.add((k, 3))
                            # heu += mins[k]
                if board[i][j + 1] != 12:
                    if all_tiles[board[i][j + 1]][3] in rs:
                        for k in rs[all_tiles[board[i][j + 1]][3]]:
                            if tile_exists[k]:
                                continue
                            # board[i][j] = k
                            # heu -= mins[k]
                            if cost + all_tiles[k][1] - mins[k] < min_cost:
                                # hq.heappush(h, (cost + all_tiles[k][1] - mins[k], state_to_number(board)))
                                options.add((k, 1))
                            # heu += mins[k]
            for k, dir in options:
                board[i][j] = k
                state_num = state_to_number(board)
                if state_num in seen:
                    continue
                hq.heappush(h, (cost + all_tiles[k][dir] - mins[k], state_num))
                # seen[state_num] = True
            board[i][j] = 12



import numpy as np
b = np.array([30, 30, 60, 60, 60, 90])

d = {}
for i in range(len(b)):
    d[b[i]] = i

ans = []
for i in range(len(b)):
    if d[b[i]] == i:
        ans.append(i)
print(ans)
