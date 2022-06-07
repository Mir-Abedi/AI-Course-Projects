import hardest_game
import random as rand
import heapq
import numpy as np

def play_game_AI(str, map_name='map1.txt'):
    game = hardest_game.Game(map_name=map_name, game_type='AI').run_AI_moves_graphic(moves=str)
    return game


def simulate(str, map_name='map1.txt'):
    game = hardest_game.Game(map_name=map_name, game_type='AI').run_AI_moves_no_graphic(moves=str)
    return game


def run_whole_generation(list_of_strs, N, map_name='map1.txt'):
    game = hardest_game.Game(map_name=map_name, game_type='AIS').run_generation(list_of_moves=list_of_strs, move_len=N)
    return game


def play_human_mode(map_name='map1.txt'):
    hardest_game.Game(map_name=map_name, game_type='player').run_player_mode()



# -------------------------------------

def cut_population(p):
    if rand.uniform(0, 1) > p:
        return
    global len_moves
    if len_moves <= 10:
        return
    for i in range(N):
        population[i] = population[i][:-10]
    len_moves -= 10

def fitness(m):
    # g = simulate(agent, m)
    # if g.hasWon:
    #     return -1
    # # temp = 30/manhattan_dist(g.end.x, g.end.y, g.player.x , g.player.y)
    # temp = 0.1
    # for i in g.goals:
    #     if i[1]:
    #         temp += 1
    # if g.hasDied:
    #     temp = temp / 2
    # return temp
    g = run_whole_generation(population, len_moves, m)
    fit = []
    for i in range(len(g.players)):
        if g.players[i][2]:
            winners[m] = population[i]
            return None
    for i in g.players:
        fit.append(1.1 - (d[(i[0].x, i[0].y)]/max_dist))

    for i in g.goal_player:
        for j in range(len(i)):
            if i[j]:
                fit[j] += 10 / max_dist
    
    dead = 0
    for i in range(len(g.players)):
        if g.players[i][1] != -1:
            dead += 1
            fit[j] /= 20
    if dead/N >= 0.6:
        cut_population(0.1)
    
    s = sum(fit)
    for i in range(len(fit)):
        fit[i] = fit[i] / s
    
    for i in range(1, len(fit)):
        fit[i] += fit[i - 1]

    return fit


def crossover(s1, s2):
    index = rand.randint(0, len(s1) - 1)
    temp1 = s1[0:index + 1] + s2[index + 1 : len(s2)]
    temp2 = s2[0:index + 1] + s1[index + 1 : len(s1)]
    return temp1, temp2

def perform_crossover(arr):
    global population
    for i in range(0, N, 2):
        population[i], population[i + 1] = crossover(arr[i], arr[i + 1])

def find_binarysearch(p, arr):
    if p <= arr[0]:
        return 0
    s = 0
    e = len(arr) - 1
    while True:
        if e - s == 1:
            return e
        middle = (e + s) // 2
        if p <= arr[middle]:
            e = middle
        else:
            s = middle

def selection(m): # returns None if won the game
    fit = fitness(m)
    if fit == None:
        return None
    selected = []
    for _ in range(N):
        chosen = rand.uniform(0, 1)
        # for i in range(len(fit) - 1):
        #     if chosen >= fit[i] and chosen <= fit[i + 1]:
        #         selected.append(population[i])
        #         break
        selected.append(population[find_binarysearch(chosen, fit)])
    return selected


def mutation(arr, p):
    if rand.uniform(0, 1) > p:
        return
    global len_moves
    len_moves += 10
    for _ in range(10):
        for i in range(len(arr)):
            arr[i] += rand.choice(list_of_moves)

def run_GA_for_map(map_name):
    global population
    population = [rand.choice(list_of_moves) for _  in range(N)]
    # index = 0 # todo remove
    while True:
        
        # index += 1
        temp = selection(map_name)
        if temp == None: # one among population has won
            return
        perform_crossover(temp)
        mutation(population, 0.7)
        
def check_point_on_border(x, y):
    for i in horizs:
        if y == i[3] and x <= i[1] and x >= i[0]:
            return True
    for i in verticals:
        if x == i[0] and y <= i[3] and y >= i[2]:
            return True
    return False

def BFS(x_start, y_start):
    global max_dist
    d = {}
    arr = [(0, x_start, y_start)]
    while arr:
        ans, x, y = arr.pop(0)
        if (x, y) in d:
            continue
        d[(x, y)] = ans
        max_dist = max(max_dist, ans)
        if check_point_on_border(x, y):
            continue
        # arr.append((x + 5, y, ans + 1))
        # arr.append((x - 5, y, ans + 1))
        # arr.append((x, y + 5, ans + 1))
        # arr.append((x, y - 5, ans + 1))
        heapq.heappush(arr, (ans + 1, x + 5, y))
        heapq.heappush(arr, (ans + 1, x - 5, y))
        heapq.heappush(arr, (ans + 1, x, y + 5))
        heapq.heappush(arr, (ans + 1, x, y - 5))

        heapq.heappush(arr, (ans + 2, x - 5, y + 5))
        heapq.heappush(arr, (ans + 2, x - 5, y - 5))
        heapq.heappush(arr, (ans + 2, x + 5, y + 5))
        heapq.heappush(arr, (ans + 2, x + 5, y - 5))

    return d


list_of_moves = ['w', 'a', 's', 'd']
N = 2000
len_moves = 1
population = [rand.choice(list_of_moves) for _  in range(N)]
winners = {}

maps = ['map2.txt' ]#, 'map2.txt', 'map3.txt']

verticals = []
horizs = []

max_dist = 0

# g = simulate('w')


# print(g.player.x)
# print(g.player.y)

# print(check_point_on_border(g.end.x + 5, g.end.y + 5))
# play_human_mode('map3.txt')

for m in maps:
    g = simulate('x', m)
    verticals = []
    for i in g.Vlines:
        verticals.append((i.x1, i.x2, i.y1, i.y2))
    horizs = []
    for i in g.Hlines:
        horizs.append((i.x1, i.x2, i.y1, i.y2))

    d = BFS(g.end.x + 5, g.end.y + 5)
    run_GA_for_map(m)