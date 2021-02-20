from numpy.core.numeric import Inf
from hex_skeleton import HexBoard
import itertools, re, sys, random
import numpy as np
import copy
import time

#### Global variables:
size = 4
deep = 6
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


def Dijkstra_heuristic(state):
        TMP_board = HexBoard(size)
        TMP_board.board = copy.deepcopy(state)
        #For red player get the min distance among all possible pairs initial/end
        univisted_set = set([x for x in state if state[x] != 1]) ## Unvisited are reds an empty
        min_distance_red = Inf
        for initial in [x for x in univisted_set if x[1] == 0]:
            for end in [x for x in univisted_set if x[1] == size - 1]: # All possible initial and end points
                visited = []
                distance_red = Shortest_path(state, 2, initial, end, visited) ## Get the min distance between two points
                if distance_red < min_distance_red:
                    min_distance_red = distance_red
        #For blue player get the min distance among all possible pairs initial/end
        univisted_set = set([x for x in state if state[x] != 2]) ## Unvisited are reds an empty
        min_distance_blue = Inf
        for initial in [x for x in univisted_set if x[0] == 0]:
            for end in [x for x in univisted_set if x[0] == size - 1]: # All possible initial and end points
                visited = []
                distance_blue = Shortest_path(state, 1, initial, end, visited) ## Get the min distance between two points
                if distance_blue < min_distance_blue:
                    min_distance_blue = distance_blue
        # Red is max, blue is min:
        heuristic_value = min_distance_blue - min_distance_red
        return(heuristic_value)
                
def Shortest_path(state, color, initial, end, visited, steps = 0, min_distance = Inf):
    #print("initial", initial)
    TMP_board = HexBoard(size)
    TMP_board.board = copy.deepcopy(state)
    TMP_board.place(initial, color)
    visited.append(initial)
    available = [x for x in set([x for x in state if state[x] in (color, 3)]) if x not in visited]
    #print("visited ", visited)
    #print("set ", set([x for x in state if state[x] in (color, 3)]))
    #print("available", available)
    #print("neighbours", TMP_board.get_neighbors(initial))
    #TMP_board.print()
    #print("neighbours", [x for x in TMP_board.get_neighbors(initial) if x in available])
    #time.sleep(2)


    if steps >= min_distance: ## Cutoff, efficiency sake
        return(Inf)
    
    if initial == end:
        #print("We reached end", steps)
        return(steps)
    else:
        if len([x for x in TMP_board.get_neighbors(initial) if x in available]) <= 0:
            #print("WHOOPS")
            #print([x for x in TMP_board.get_neighbors(initial) if x in available])
            #print(len([x for x in TMP_board.get_neighbors(initial) if x in available]) )
            return(Inf) #If there is no more options in that branch
        for neighbour in [x for x in TMP_board.get_neighbors(initial) if x in available]:
            #print("Neighbour", neighbour)
            if TMP_board.get_color(neighbour) == color:
                min_distance = min(min_distance, Shortest_path(state, color, neighbour, end, visited, steps, min_distance))
            elif TMP_board.get_color(neighbour) == 3:
                min_distance = min(min_distance, Shortest_path(state, color, neighbour, end, visited, steps + 1, min_distance)) 
        return(min_distance)

def eval(state):
    # In order to use the functions in hex
    # I create a temp object and add the state
    TMP_board = HexBoard(size)
    TMP_board.board = copy.deepcopy(state)
    if TMP_board.is_game_over() or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0:
        print("LEAF")
        if TMP_board.check_win(2):
            return(1)
        elif TMP_board.check_win(1):
            return(-1)
        else:
            return(0)
    else:
        #print("Heuristic evaluation")
        #value = (random.uniform(-1,1)) ## Random evaluation is this is not a LEAF node.
        value = Dijkstra_heuristic(state)
        #print(value)
        return(value)

## Minimax implementation:
# TODO Transposition Tables
# TODO Iterative Deepening
# TODO Some way of visualize the tree and cutoffs


def minimax(state, d, alpha = -Inf, beta = Inf): # Returns the value of the LEAF following optimal play for both players 
    # ALPHA-BETHA WIDE WINDOW (IMPROVE??)
    # In order to use the functions in hex
    # I create a temp object and add the state

    TMP_board = HexBoard(size)
    TMP_board.board = copy.deepcopy(state)
    if d <= 0:
        return(eval(state))
    else:
        if sum([TMP_board.is_color(x, 1) for x in TMP_board.board]) >= \
                sum([TMP_board.is_color(x, 2) for x in TMP_board.board]): ## Just Check turn
            
            value = -Inf  # MAX PLAYER/NODE
            if TMP_board.is_game_over() or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0: # IF IT IS A LEAF
                return(eval(state))
            else:
                #print("Max node branches:")
                for action in getMoveList(state): # Assessing a MAX NODE
                    #print(action)
                    value = max(value, minimax(result(state, action), d-1, alpha, beta))
                    alpha = max(value, alpha)
                    if alpha >= beta: # Because action is gonna have a reward as high as beta.
                        #print("Beta cutoff")
                        break
                return(value)
                    

        else:
        
            value = Inf # MIN PLAYER/NODE
            if TMP_board.is_game_over() or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0: # IF IT IS A LEAF
                return(eval(state))   
            else:
                #print("Min node branches:")
                for action in getMoveList(state):
                    #print(action)
                    value = min(value, minimax(result(state, action), d-1, alpha, beta))
                    beta = min(value, beta)
                    if alpha >= beta: # Because the action is gonna have a reward as low as alpha
                        #print("Alpha cutoff")
                        break
                return(value)
        

def MakeMove(board, color):
    state = copy.deepcopy(board.board)
    if color == 2:
        Best_outcome = -Inf
        Best_move = None

        for action in getMoveList(state):
            print("Searching... : ", action)
            U = max(Best_outcome, minimax(result(state, action), d = deep)) ## Default -inf inf window
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
            U = min(Best_outcome, minimax(result(state, action), d = deep)) ## Default -inf inf window
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
    while (user_move, color) not in moves:
        response = re.match( ar * 2, input("Move: "))
        user_move = (int(response[1]), int(response[2])) # It is X and Y
        
        if response and board.is_empty(user_move):
            board.place(user_move, color)
            moves.append((user_move, color))

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
        if moves[-1][1] == User_color:# If the last move was from USER
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





