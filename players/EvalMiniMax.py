import random
import numpy as np

from Utils import *

class EvalMiniMax:
    def __init__(self, player, max_depth = 3, evalType = 1):
        self.player = player  # Player value (e.g., 1 for white, -1 for black)
        self.max_depth = max_depth
        
        self.setPieceScores(evalType)
        

    def move(self, env):
        validMoves = get_valid_moves(env.board, self.player)
        if validMoves == []:
            return
        
        board = env.get_board()
        best_score = -np.inf
        best_move = None
        player = self.player

        if len(validMoves) == 1:
            best_move = validMoves[0]
        else:
            for move in validMoves:
                score = self.negamax_alphabeta(update_board(board, player, move), 1, player, env, -np.inf, np.inf)
                if score > best_score or score == best_score == -np.inf:
                    best_score = score
                    best_move = move

        env.make_move(best_move, self.player)

    
    # Variant of minimax that condenses it down to one function recursion, instead of two calling each other
    # We found negamax on wikipedia: https://en.wikipedia.org/wiki/Negamax
    def negamax_alphabeta(self, board, depth, player, env, alpha, beta):
        if is_game_over(board): return who_won(board) * player * np.inf
        if depth == self.max_depth: return self.evaluate(board, player)
    
        score = -np.inf
        for move in get_valid_moves(board, -player):
            score = max(score, -self.negamax_alphabeta(update_board(board, -player, move),  depth+1, -player, env, -beta, -alpha))
            alpha = max(alpha, score)
            if (alpha >= beta):
                break
        return score
    
    def evaluate(self, board, player):
        return np.sum(player * board * self.piece_scores)
    
    def setPieceScores(self, evalType):
        match evalType:
            case 1:
                piece_scores_4x4 = np.array([
                    [10, 3, 3, 3],
                    [3, 1, 1, 1],
                    [3, 1, 1, 1],
                    [3, 1, 1, 1]
                ])

            case 2:
                piece_scores_4x4 = np.array([
                    [4, -3, 2, 2],
                    [-3, -4, -1, -1],
                    [2, -1, 1, 0],
                    [2, -1, 0, 1]
                ])
            case _:
                raise Exception("Invalid evalType") 

        self.setPieceScoresFrom4x4(piece_scores_4x4)
        
    def setPieceScoresFrom4x4(self, piece_scores_4x4):
        # Construct remaining quadrants
        mirrored_horizontal = piece_scores_4x4[:, ::-1]  # upper right
        mirrored_vertical = piece_scores_4x4[::-1]       # lower left
        mirrored_both = mirrored_horizontal[::-1]        # lower right
        # Combine
        self.piece_scores = np.block([
            [piece_scores_4x4, mirrored_horizontal],
            [mirrored_vertical, mirrored_both]
        ])