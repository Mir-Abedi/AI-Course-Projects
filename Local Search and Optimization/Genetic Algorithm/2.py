import hardest_game
import random as rand

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


play_game_AI('wdswadwdaadddwawswddddssasdawwsadaaawwdawdwsdaawwwwdsawwdaaaaswsdswsddwawwdwwwwdsddadddwssdsddasdwwswsdwswdasaaawdssdasddwsdwwawaaswawadwawddaadswwassw', 'map3.txt')
