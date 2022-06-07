import time

def row_constraint(i, j):
    ans = []
    for k in range(9):
        if k == i:
            continue
        ans.append((k, j))
    return ans

def col_constraint(i, j):
    ans = []
    for k in range(9):
        if k == j:
            continue
        ans.append((i, k))
    return ans

def square_constraints(i, j): # returns square containing (i, j) ignoring row and col
    ans = []
    for k in range((i//3)*3, (i//3)*3 + 3):
        for l in range((j//3)*3, (j//3)*3 + 3):
            if k == i or l == j:
                continue
            ans.append((k, l))
    return ans

def calculate_CV(i, j):
    ret = 0
    for k, l in adj_list[i][j]:
        if not determined[k][l]:
            ret += 1
    return ret

def choose_next(): # returns next (i, j) based on MRV and then LCV
    candids = []
    m = 10
    for i in range(9):
        for j in range(9):
            if determined[i][j]:
                continue
            if sum(available_values[i][j]) < m:
                candids = [(i, j)]
                m = sum(available_values[i][j])
            elif sum(available_values[i][j]) == m:
                candids.append((i, j))
    # MRV complete

    i_chosen, j_chosen = -1, -1
    m = 50

    for i, j in candids:
        cv = calculate_CV(i, j)
        if cv <= m:
            i_chosen, j_chosen = i, j
            m = cv
    return i_chosen, j_chosen

def AC_3(): # arc consistency
    p_i, p_j = -1, -1
    while True:
        done = False
        for i in range(9):
            for j in range(9):
                if sum(available_values[i][j]) == 1 and not determined[i][j]:
                    if i == p_i and j == p_j:
                        return
                    index = -1
                    for k in range(9):
                        if available_values[i][j][k]:
                            index = k
                            break
                    for k, l in adj_list[i][j]:
                        if determined[k][l]:
                            continue
                        available_values[k][l][index] = False
                    done = True
                    p_i, p_j = i, j
                    break
            if done:
                break
        if not done:
            return


def is_done():
    for i in range(9):
        for j in range(9):
            if not determined[i][j]:
                return False
    return True

def copy_available_values(arr):
    ret = [[[True] * 9 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            for k in range(9):
                ret[i][j][k] = arr[i][j][k]
    return ret

def backtrack_solve():
    global available_values
    if is_done():
        for i in range(9):
            for j in range(9):
                print(f'{final_value[i][j]} ', end='')
            print('')
        print((time.time_ns() - t)/1000000)
        exit(0)

    AC_3() # arc consistency

    temp = copy_available_values(available_values)

    r, c = choose_next() # choose next tile

    for i in range(9):
        if available_values[r][c][i]:
            determined[r][c] = True
            final_value[r][c] = i + 1
            for k, l in adj_list[r][c]:
                available_values[k][l][i] = False
            backtrack_solve()
            available_values = temp
            final_value[r][c] = -1
            determined[r][c] = False

final_value = [[-1] * 9 for _ in range(9)]
adj_list = [[[] for _ in range(9)] for _ in range(9)]
determined = [[False] * 9 for _ in range(9)]
available_values = [[[True] * 9 for _ in range(9)] for _ in range(9)]

for i in range(9):
    for j in range(9):
        adj_list[i][j].extend(row_constraint(i, j))
        adj_list[i][j].extend(col_constraint(i, j))
        adj_list[i][j].extend(square_constraints(i, j))

for i in range(9):
    temp = input().split()
    for j in range(9):
        if temp[j] == '.':
            continue
        final_value[i][j] = int(temp[j])
        determined[i][j] = True
        for k, l in adj_list[i][j]:
            available_values[k][l][final_value[i][j] - 1] = False

t = time.time_ns()
backtrack_solve()




