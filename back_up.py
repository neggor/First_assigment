from numpy.core.numeric import Inf
from hex_skeleton import HexBoard
import itertools, re, sys, random, keyboard
import numpy as np
import copy
import time
import pdb

#### Global variables:
size = 6
think_time = 5
zobTable = [[[random.randint(1,2**64 - 1) for i in range(2)]for j in range(size)]for k in range(size)]
my_board = HexBoard(size)
all_positions = list(itertools.product(range(size), repeat= 2))
moves = []
transposition_table = {}
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
        univisted_set = set([x for x in state if state[x] != 1]) 
        min_distance_red = Inf
        for initial in [x for x in univisted_set if x[1] == 0]:
            for end in [x for x in univisted_set if x[1] == size - 1]:
                distance = {}
                visited = []
                predecessor = {} 
                distance_red = shortest_path(generate_graph(state, 2), initial, end, distance, visited, predecessor)
                if distance_red < min_distance_red:
                    min_distance_red = distance_red
        univisted_set = set([x for x in state if state[x] != 2]) 
        min_distance_blue = Inf
        for initial in [x for x in univisted_set if x[0] == 0]:
            for end in [x for x in univisted_set if x[0] == size - 1]: 
                distance = {}
                visited = []
                predecessor = {}
                distance_blue = shortest_path(generate_graph(state, 1), initial, end, distance, visited, predecessor)
                if distance_blue < min_distance_blue:
                    min_distance_blue = distance_blue

        if sum([TMP_board.is_color(x, 1) for x in TMP_board.board]) >= \
                sum([TMP_board.is_color(x, 2) for x in TMP_board.board]):
            print("BLUE")
            heuristic_value = min_distance_blue
        else:
            print("RED")
            heuristic_value = -min_distance_red
        return(heuristic_value)



def generate_graph(state, color):
    TMP_board = HexBoard(size)
    TMP_board.board = state
    available = [x for x in state if (state[x] == 3 or state[x] == color)]
    costs = {}
    graph = {}
    for node in available:
        # Assing values:
        if TMP_board.board[node] == color:
            costs[node] = 0
        else:
            costs[node] = 1

        # Not include isolated nodes in the graph:
        if all([(TMP_board.board[x]!= color and TMP_board.board[x] != 3) for x in TMP_board.get_neighbors(node)]):
            print("HEY!")
            continue 

        graph[node] = ({}, costs[node])

    for node in available:
        for neighbour in TMP_board.get_neighbors(node):
                if neighbour in available and neighbour in costs:
                    graph[node][0].update({neighbour:costs[neighbour]})

    return(graph)

def shortest_path(graph, initial, end, distance = {}, visited = [], predecessor = {}):
    if initial not in graph:
        return Inf
    if end not in graph:
        return Inf
    if initial == end:
        if initial not in distance:
            return Inf
        output = distance[initial]
        return(output)
        # Code inspired by: http://www.gilles-bertrand.com/2014/03/dijkstra-algorithm-python-example-source-code-shortest-path.html
    else:
        if not visited:
            distance[initial] = graph[initial][1]
        
        for neighbour in graph[initial][0]: # For each neighbour
            if neighbour not in visited: # If it is in visited
                new_distance = distance[initial] 
                new_distance = new_distance + graph[initial][0][neighbour] # Calculate the new distance of my position + the next position
                if new_distance < distance.get(neighbour, Inf): # To check that I am reaching that node for the shortest path
                    distance[neighbour] = new_distance
                    predecessor[neighbour] = initial

        visited.append(initial)
        unvisited = {}
        for node in graph:
            if node not in visited:
                unvisited[node] = distance.get(node, Inf)

        next = min(unvisited, key = unvisited.get)
        length = shortest_path(graph, next, end, distance, visited, predecessor)
        return(length)


def eval(state):
    # In order to use the functions in hex
    # I create a temp object and add the state
    TMP_board = HexBoard(size)
    TMP_board.board = copy.deepcopy(state)
    if TMP_board.check_win(2) or TMP_board.check_win(1) or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0:
        if TMP_board.check_win(2):
            return(100)
        elif TMP_board.check_win(1):
            return(-100)
        else:
            return(0)
    else:
        value = Dijkstra_heuristic(state)
        return(value)

## Minimax implementation:
# TODO Transposition Tables
# TODO Iterative Deepening
# TODO Some way of visualize the tree and cutoffs

## Transposition table stuff:
# Next two functions inspired by: https://iq.opengenus.org/zobrist-hashing-game-theory/
###############
def indexing(piece):
    if (piece == 1):
        return 0
    if (piece == 2):
        return 1
    else:
        return -1 

def computeHash(state):
    h = 0
    for i in state:
            if state[i] != 3:
                piece = indexing(state[i])
                h ^= zobTable[i[0]][i[1]][piece]
    return h
#############

def minimax(state, d, start, alpha = -Inf, beta = Inf): # Returns the value of the LEAF following optimal play for both players 
    # ALPHA-BETHA WIDE WINDOW (IMPROVE??)
    # In order to use the functions in hex
    # I create a temp object and add the state
    TMP_board = HexBoard(size)
    TMP_board.board = copy.deepcopy(state)
    end = time.time()
    best_move_tt = [None]
    bm = None
    if computeHash(state) in transposition_table: # I have already reached this position at this depth.
        #pdb.set_trace()
        if d == transposition_table[computeHash(state)]["depth"]:
            print("Hit!")
            return(transposition_table[computeHash(state)]["value"])
        else:
            best_move_tt = [transposition_table[computeHash(state)]["b_move"]] ## I expect that the best move for a shallower search is a good estimation of the good move in a deeper one.
    
    if  keyboard.is_pressed("p") or (end - start) >= think_time:
        return(eval(state))
    if d <= 0:
        return(eval(state))
    else:
        if sum([TMP_board.is_color(x, 1) for x in TMP_board.board]) >= \
                sum([TMP_board.is_color(x, 2) for x in TMP_board.board]): ## Just Check turn
            
            value = -Inf  # MAX PLAYER/NODE
            if TMP_board.check_win(2) or TMP_board.check_win(1) or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0: # IF IT IS A LEAF
                return(eval(state))
            else:
                for action in best_move_tt + getMoveList(state): # Assessing a MAX NODE
                    if action is None:
                        continue
                    value_c = minimax(result(state, action), d-1, start, alpha, beta)
                    if value_c > value:
                        bm = action
                        value = value_c
                    alpha = max(value, alpha)
                    if alpha >= beta: # Because action is gonna have a reward as high as beta.
                        break
                
                    

        else:
        
            value = Inf # MIN PLAYER/NODE
            if TMP_board.check_win(2) or TMP_board.check_win(1) or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0: # IF IT IS A LEAF
                return(eval(state))   
            else:
                for action in best_move_tt + getMoveList(state):
                    if action is None:
                        continue
                    value_c = minimax(result(state, action), d-1, start, alpha, beta)
                    if value_c < value:
                        bm = action
                        value = value_c
                    alpha = max(value, alpha)
                    if alpha >= beta: # Because the action is gonna have a reward as low as alpha
                        break
        transposition_table[computeHash(state)] = {"depth":d, "b_move":bm, "value":value}
        return(value)
        


def MakeMove(board, color):
    state = copy.deepcopy(board.board)
    d = 0
    start = time.time()
    end = 0
    best_move_tt = [None]
    if computeHash(state) in transposition_table:
        if d == transposition_table[computeHash(state)]["depth"]:
            board.place([transposition_table[computeHash(state)]["b_move"]], color) # If we know already the best move
        else:
            best_move_tt = [transposition_table[computeHash(state)]["b_move"]]
    
    while not keyboard.is_pressed("p") and (end - start) < think_time:
        d = d + 1
        print("Depth", d)
        if color == 2:
            Best_outcome = -Inf
            Best_move = None

            for action in best_move_tt + getMoveList(state):
                if action is None:
                    continue
                print("Searching... : ", action)
                U = max(Best_outcome, minimax(result(state, action), d = d, start = start)) ## Default -inf inf window
                print(U)
                if U > Best_outcome:
                    Best_outcome = U
                    Best_move = action
            moves.append((Best_move, color))
            
        
        elif color == 1:
            Best_outcome = Inf
            Best_move = None

            for action in best_move_tt + getMoveList(state):
                if action is None:
                    continue
                print("Searching... : ", action)
                U = min(Best_outcome, minimax(result(state, action), d = d, start = start)) ## Default -inf inf window
                print(U)
                if U < Best_outcome:
                    Best_outcome = U
                    Best_move = action
            moves.append((Best_move, color))
        end = time.time()

    transposition_table[computeHash(state)] = {"depth":d, "b_move":Best_move, "value":Best_outcome}
    board.place(Best_move, color)
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





 