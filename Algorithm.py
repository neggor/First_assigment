from numpy.core.numeric import Inf
from hex_skeleton import HexBoard
import itertools, re, sys, random
import numpy as np
import copy


#### Global variables:
size = 3
my_board = HexBoard(size)
all_positions = list(itertools.product(range(size), repeat= 2))
moves = []
####



def getMoveList(state): # Return all available moves in a given board
    # In order to use the functions in hex
    # I create a temp object and add the state
    TMP_board = HexBoard(size)
    TMP_board.board = state
    return[available for available in all_positions if
     TMP_board.is_empty(available)]


def player(state): # Return the color of the player
    # In order to use the functions in hex
    # I create a temp object and add the state
    TMP_board = HexBoard(size)
    TMP_board.board = state
    if sum([TMP_board.is_color(x, 1) for x in TMP_board.board]) >= \
            sum([TMP_board.is_color(x, 2) for x in TMP_board.board]):
        return(2)
    else:
        return(1)


def result(board, action): # Update the board
    if board[action] != 3:
        raise Exception("Non empty cell")
    new_board = copy.deepcopy(board)
    new_board[action] = player(new_board)
    return(new_board)



def eval(state):
    # In order to use the functions in hex
    # I create a temp object and add the state
    
    TMP_board = HexBoard(size)
    TMP_board.board = state
    if TMP_board.check_win(2):
        return(1)
    elif TMP_board.check_win(1):
        return(-1)
    else:
        return(0)


## TODO transposition table in order to make iterative deepening

## Minimax implementation:
# TODO ALPHA-BETA pruning

def minimax(state): # Returns the value of the LEAF following optimal play for both players
    # In order to use the functions in hex
    # I create a temp object and add the state
    TMP_board = HexBoard(size)
    TMP_board.board = state
    #TMP_board.print()
    if sum([TMP_board.is_color(x, 1) for x in TMP_board.board]) >= \
            sum([TMP_board.is_color(x, 2) for x in TMP_board.board]): ## Just Check turn
        
        value = -Inf  # MAX PLAYER/NODE
        if TMP_board.is_game_over() or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0: # IF IT IS A LEAF
            return(eval(state))
        else:
            for action in getMoveList(state):
                value = max(value, minimax(result(state, action)))
            return(value)
                

    else:
      
        value = Inf # MIN PLAYER/NODE
        if TMP_board.is_game_over() or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0: # IF IT IS A LEAF
            return(eval(state))   
        else:
            for action in getMoveList(state):
                value = min(value, minimax(result(state, action)))
            return(value)
    

def MakeMove(board, color):
    state = copy.deepcopy(board.board)
    if color == 2:
        Best_outcome = -Inf
        Best_move = None

        for action in getMoveList(state):
            print("Searching... : ", action)
            U = max(Best_outcome, minimax(result(state, action)))
            print(U)
            if U > Best_outcome:
                Best_outcome = U
                Best_move = action
        board.place(Best_move, color)
        moves.append((Best_move, color))
        return(board.print())
    
    elif color == 1:
        Best_outcome = Inf
        Best_move = None

        for action in getMoveList(state):
            print("Searching... : ", action)
            U = min(Best_outcome, minimax(result(state, action)))
            print(U)
            if U < Best_outcome:
                Best_outcome = U
                Best_move = action
        board.place(Best_move, color)
        moves.append((Best_move, color))
        return(board.print())

                
## Interface
def user_query(board, color):
    ar = '([0-%s])' %(board.size)
    user_move = None
    while user_move not in board.board:
        response = re.match( ar * 2, input("Move: "))
        user_move = (int(response[2]), int(response[1])) # I have inverted this because is more 
                                                         # confortable with the order rows and columns
        moves.append((user_move, color))
        if response and board.is_empty(user_move):
            board.place(user_move, color)

        else:
            print("Insert a valid move")
    return(board.print())


## TODO various checks for empty tiles to encapsulate the raw board data structure management, and
# of course functions to help debugging, such as board printers.

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
        user_query(my_board, User_color)
    else:
        MakeMove(my_board, AI_color)
    
    while not my_board.is_game_over():
        if moves[-1][1] == User_color : # If the last move was from USER
            print("AI turn")
            MakeMove(my_board, AI_color)
        else:
            user_query(my_board, User_color)
    if my_board.check_win(User_color):
        print("You win")
        return()
    else:
        print("AI wins")
        return()

if __name__ == '__main__':
    main()





