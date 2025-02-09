import time
import tkinter as tk
import numpy as np
from sys import argv

from Graphics import Graphics
from Othello import Othello
from players import *
from Utils import *

# not global?
n = 8
white_value = 1
black_value = -1


def getPlayerType(arg, player_value , graphics, max_depth):
    arg = arg.lower()
    match arg:
        case "h":
            return HumanPlayer(player_value, graphics)
        case "b1":
            return EvalMiniMax(player_value, max_depth, 1)
        case "b2":
            return EvalMiniMax(player_value, max_depth, 2)
        case "r":
            return RandomPlayer(player_value)
        case _ :
            raise Exception("Invalid player input: h for human player, b for bot player (minimax) and r for random player") 

def get_depth(time_limit):
    marginal_factor = 1.5
    depth = (4.24086193 + 0.5964272 * np.log(time_limit) ) * 1/marginal_factor
    return np.floor(depth)

def analyze_times(times):
        print()
        percentile_95 = np.percentile(times, 95)
        print("95th Percentile (95% of times are less than or equal to this value):", percentile_95)

        #  depth 1: 0.0030129551887512207
        #  depth 2: 0.03724727630615232
        #  depth 3: 0.12645692825317364
        #  depth 4: 0.8725171566009519
        #  depth 5: 2.702528178691864
        #  depth 6: 17.323252332210533

def print_last_game_result(sum, n_played):
    if sum == 0:
        print(f"- Game {n_played}: result: Draw")
        return
    winnner_string = "Black_player" if sum > 0 else "White_player"
    print(f"- Game {n_played}: result: {winnner_string} won by {np.abs(sum)} discs")    
        

def main():

    graphics = Graphics()
    env = Othello()

    if len(argv) >= 1:
        try:
            n_games = int(argv[1])
            time_limit = float(argv[2])
            max_depth = get_depth(time_limit)
            black_player = getPlayerType(argv[3], black_value, graphics, max_depth)
            white_player = getPlayerType(argv[4], white_value, graphics, max_depth)
            
        except: 
            print("Invalid input, standards initialisation used instead")
            n_games = 1
            time_limit = 1
            max_depth = get_depth(time_limit)
            black_player = HumanPlayer(black_value, graphics)
            white_player = EvalMiniMax(white_value, max_depth)


    n_wins = {
        white_value: 0,
        0: 0,
        black_value: 0
    }

    n_played = 0

    black_player_time_list = []
    white_player_time_list = []
    
    start_time = time.time()
    while n_played < n_games:
        env.reset()
        graphics.draw(env.board)
        while True:
            
            t_start = time.time()
            black_player.move(env)
            black_player_time_list.append(time.time()-t_start)

            graphics.draw(env.board)
            if is_game_over(env.board): break

            
            t_start = time.time()
            white_player.move(env)
            white_player_time_list.append(time.time()-t_start)

            graphics.draw(env.board)
            if is_game_over(env.board): break
        
        winner = who_won(env.board)
        n_wins[winner] += 1
        n_played += 1
        if n_games > 1:
            print_last_game_result(np.sum(env.board), n_played)
            
    
    elapsed_time = time.time() - start_time
    graphics.root.quit()

    print()
    print('Results:')
    print(f'Black_player won {100.0 * n_wins[black_value] / n_played}%')
    print(f'White_player won {100.0 * n_wins[white_value] / n_played}%')
    print(f'Draw             {100.0 * n_wins[0] / n_played}%')
    print()
    print(f"Total elapsed time: {elapsed_time:.6f} seconds")
    print(f"Average elapsed time: {elapsed_time/n_played:.6f} seconds")


    #analyze_times(black_player_time_list)
    #analyze_times(white_player_time_list)
        


if __name__ == "__main__": main()