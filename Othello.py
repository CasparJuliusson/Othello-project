import numpy as np
from Utils import *


# not global?
n = 8
white_value = 1
black_value = -1

class Othello:
    def __init__(self):
        self.board = np.zeros((n, n), dtype=int)
        self.directions = [(-1,-1), (-1,0), (-1,1),
                           (0,-1),          (0,1),
                           (1,-1),  (1,0) , (1,1)]


    def get_board(self):
        return self.board.copy()

    def reset(self):
        self.board[:,:] = 0
        self.board[3][3] = self.board[4][4] = white_value
        self.board[3][4] = self.board[4][3] = black_value
        self.winner = 0

    
    def make_move(self, move, player): #  not that happy about having two of these (updateboard in utils)
        x = move[0]        
        y = move[1]    

        self.board[x][y] = player
        opponent = -player
        
        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            to_flip = []
            while is_valid_position(nx, ny) and self.board[nx][ny] == opponent:
                to_flip.append((nx, ny))
                nx += dx
                ny += dy
                
            if is_valid_position(nx, ny) and self.board[nx][ny] == player:
                for (fx, fy) in to_flip:
                    self.board[fx][fy] = player