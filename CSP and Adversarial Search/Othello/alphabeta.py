from player import Player
from random import shuffle
import numpy as np


minus_inf = -(10**10)
inf = -1*minus_inf

class AlphaBetaPlayer(Player):
    def get_next_move(self):
        d = 7
        self.board.start_imagination()
        if self.player_number == 0:
            return max_find_move(d, minus_inf - 1, inf + 1, 0, self.board)[1]
        return min_find_move(d, minus_inf - 1, inf + 1, 1, self.board)[1]

def get_other_player(p_num):
    return 1 - p_num

def util(board): # returns black util
    n = board.get_n()
    b = 0
    w = 0
    u = 0
    for i in range(n):
        for j in range(n):
            if board.imaginary_board_grid[i, j] == 0:
                b += 1
                u += get_point_cell(i, j, n)
            elif board.imaginary_board_grid[i, j] == 1:
                w += 1
                u -= get_point_cell(i, j, n) 
    return (0.25*(b - w)) + (0.75*u)

def get_point_cell(i, j, n):
    if (i == 0 and j == 0) or (i == 0 and j == n - 1) or (i == n - 1 and j == 0) or (i == n - 1 and j == n - 1):
        return 1000
    elif i == 0 or j == 0 or i == n - 1 or j == n - 1:
        return 500
    return 1
    

def end_game_util(board):
    n = board.get_n()
    b = 0
    w = 0
    for i in range(n):
        for j in range(n):
            if board.imaginary_board_grid[i, j] == 0:
                b += 1
            elif board.imaginary_board_grid[i, j] == 1:
                w += 1
    if b > w:
        return 1000000
    elif b == w:
        return 0
    return -1000000

def player_has_move(board, player_num):
    n = board.get_n()
    for i in range(n):
        for j in range(n):
            if board.is_imaginary_move_valid(player_num, i, j):
                return True
    return False


def max_find_move(depth, alpha, beta, player_num, board): # returns value, move -> (i, j)  if no move : returns None
    if depth == 0:
        return util(board), None
    
    valid_moves = []
    n = board.get_n()

    for i in range(n):
        for j in range(n):
            if board.is_imaginary_move_valid(player_num, i, j):
                valid_moves.append((i, j))

    if not valid_moves: # empty moves
        if not player_has_move(board, get_other_player(player_num)):
            return end_game_util(board), None
        return -500000, None # black has no move but white can move -> defeat
    
    # one or more moves exist :
    shuffle(valid_moves)

    v = minus_inf
    chosen_move = None
    for i, j in valid_moves:
        temp = np.copy(board.imaginary_board_grid)
        board.imagine_placing_piece(player_num, i, j)
        temp1 = min_find_move(depth - 1, alpha, beta, get_other_player(player_num), board)[0]
        if temp1 >= v:
            v = temp1
            chosen_move = (i, j)
        board.imaginary_board_grid = temp # revert move
        if v >= beta:
            break
        alpha = max(alpha, v)
    return v, chosen_move


def min_find_move(depth, alpha, beta, player_num, board):
    if depth == 0:
        return util(board), None
    
    valid_moves = []
    n = board.get_n()

    for i in range(n):
        for j in range(n):
            if board.is_imaginary_move_valid(player_num, i, j):
                valid_moves.append((i, j))

    if not valid_moves: # empty moves
        if not player_has_move(board, get_other_player(player_num)):
            return end_game_util(board), None
        return -500000, None # black has no move but white can move -> defeat
    
    # one or more moves exist :
    shuffle(valid_moves)

    v = inf
    chosen_move = None
    for i, j in valid_moves:
        temp = np.copy(board.imaginary_board_grid)
        board.imagine_placing_piece(player_num, i, j)
        temp1 = max_find_move(depth - 1, alpha, beta, get_other_player(player_num), board)[0]
        if temp1 <= v:
            v = temp1
            chosen_move = (i, j)
        board.imaginary_board_grid = temp # revert move
        if v <= alpha:
            break
        beta = min(beta, v)
    return v, chosen_move