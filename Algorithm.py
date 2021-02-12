from numpy.core.numeric import Inf
from hex_skeleton import HexBoard
import itertools, re, sys, random
import numpy as np



#### Global variables:
size = 4
board = HexBoard(size)
all_positions = list(itertools.permutations(range(0, board.size), 2))
####


# Random number generator evaluation
def eval(): # EVAL IS BLIND (TMP)
    return(random.random())

## Move generator
def getMoveList(board): ## Return all available moves in a given board
    if not (isinstance(board, HexBoard)):
        raise Exception("Use HexBoard class")
    return[available for available in all_positions if
     board.is_empty(available)]


def Make_move(board, color): ## No Minimax implemented (#TMP)
    g = -Inf
    for mov in getMoveList(board):
        a = max(g, eval()) ## EVAL IS BLIND (TMP)
        if a > g:
            best_move = mov
            g = a
    board.place(best_move, color)
    return(board.print())

## Interface
def user_query(board, color):
    ar = '([0-%s])' %(board.size)
    user_move = None
    while user_move not in board.board:
        response = re.match( ar * 2, input("Move: "))
        user_move = (int(response[1]), int(response[2]))
        if response and board.is_empty(user_move):
            board.place(user_move, color)

        else:
            print("Insert a valid move")
    return(board.print())


def main():
    ## Query for color
    User_color = re.match('BLUE|RED', input('Your color:'))
    # Change to numbers:
    if User_color[0] == 'RED': 
        User_color = 2
        AI_color = 1
    else:
        User_color = 1
        AI_color = 2
    
    # Red Begins
    if User_color == 2:
        user_query(board, User_color)
    else:
        Make_move(board, AI_color)
    while board.is_game_over or \
    len(board.board) < len(all_positions): ## Game over or full board check
        if sum([board.is_color(x, User_color) for x in board.board]) > \
            sum([board.is_color(x, AI_color) for x in board.board]):
            print("AI turn")
            Make_move(board, AI_color)
        else:
            user_query(board, User_color)

if __name__ == '__main__':
    main()





