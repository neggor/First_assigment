from hex_skeleton import HexBoard
from numpy.core.numeric import Inf
import itertools, re, sys, random
import copy

class AGENT:

    def __init__(self, board_size, depth, heuristic = False):
        self.size = board_size
        self.depth = depth
        self.heuristic = heuristic
        self.all_positions = list(itertools.product(range(self.size), repeat= 2))

    def getMoveList(self, state): # Return all available moves in a given board
        TMP_board = HexBoard(self.size)
        TMP_board.board = state
        return[available for available in self.all_positions if
        TMP_board.is_empty(available)]

    def player(self, state): # Return the color of the player
        TMP_board = HexBoard(self.size)
        TMP_board.board = state
        if sum([TMP_board.is_color(x, 1) for x in TMP_board.board]) >= \
                sum([TMP_board.is_color(x, 2) for x in TMP_board.board]):
            return(2)
        else:
            return(1)

    def result(self, board, action): # Update the board
        if board[action] != 3:
            raise Exception("Non empty cell")
        new_board = copy.deepcopy(board)
        new_board[action] = self.player(new_board)
        return(new_board)
    
    def Dijkstra_heuristic(self, state):
        TMP_board = HexBoard(self.size)
        TMP_board.board = copy.deepcopy(state)
        univisted_set = set([x for x in state if state[x] != 1])
        min_distance_red = Inf
        for initial in [x for x in univisted_set if x[1] == 0]:
            for end in [x for x in univisted_set if x[1] == self.size - 1]:
                visited = []
                distance_red = self.Shortest_path(state, 2, initial, end, visited) 
                if distance_red < min_distance_red:
                    min_distance_red = distance_red
        univisted_set = set([x for x in state if state[x] != 2]) 
        min_distance_blue = Inf
        for initial in [x for x in univisted_set if x[0] == 0]:
            for end in [x for x in univisted_set if x[0] == self.size - 1]: 
                visited = []
                distance_blue = self.Shortest_path(state, 1, initial, end, visited) 
                if distance_blue < min_distance_blue:
                    min_distance_blue = distance_blue
        heuristic_value = min_distance_blue - min_distance_red
        return(heuristic_value)
                    
    def Shortest_path(self, state, color, initial, end, visited, steps = 0, min_distance = Inf):
        TMP_board = HexBoard(self.size)
        TMP_board.board = copy.deepcopy(state)
        TMP_board.place(initial, color)
        visited.append(initial)
        available = [x for x in set([x for x in state if state[x] in (color, 3)]) if x not in visited]
        if steps >= min_distance: 
            return(Inf)
        
        if initial == end:
            return(steps)
        else:
            if len([x for x in TMP_board.get_neighbors(initial) if x in available]) <= 0:
                return(Inf) 
            for neighbour in [x for x in TMP_board.get_neighbors(initial) if x in available]:
                if TMP_board.get_color(neighbour) == color:
                    min_distance = min(min_distance, self.Shortest_path(state, color, neighbour, end, visited, steps, min_distance))
                elif TMP_board.get_color(neighbour) == 3:
                    min_distance = min(min_distance, self.Shortest_path(state, color, neighbour, end, visited, steps + 1, min_distance)) 
            return(min_distance)
            


    def eval(self, state):
        TMP_board = HexBoard(self.size)
        TMP_board.board = state
        if TMP_board.is_game_over() or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0:
            if TMP_board.check_win(2):
                return(1)
            elif TMP_board.check_win(1):
                return(-1)
            else:
                return(0)
        else:
            if self.heuristic:
                print("Dijkstra")
                return(self.Dijkstra_heuristic(state))
            else:
                print("Random")
                return(random.uniform(-1,1))

    def minimax(self, state, d, alpha = -Inf, beta = Inf): # Returns the value of the LEAF following optimal play for both players 
        TMP_board = HexBoard(self.size)
        TMP_board.board = state
        if d <= 0:
            return(eval(state))
        else:
            if sum([TMP_board.is_color(x, 1) for x in TMP_board.board]) >= \
                    sum([TMP_board.is_color(x, 2) for x in TMP_board.board]): 
                value = -Inf  
                if TMP_board.is_game_over() or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0: 
                    return(eval(state))
                else:
                    for action in self.getMoveList(state): 
                        value = max(value, self.minimax(self.result(state, action), d-1, alpha, beta))
                        alpha = max(value, alpha)
                        if alpha >= beta: 
                            break
                    return(value)
            else:
                value = Inf 
                if TMP_board.is_game_over() or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0: 
                    return(eval(state))   
                else:
                    for action in self.getMoveList(state):
                        value = min(value, self.minimax(self.result(state, action), d-1, alpha, beta))
                        beta = min(value, beta)
                        if alpha >= beta: 
                            break
                    return(value)
        
    def MakeMove(self, board, color): # Make a move using AI # FIXME
        state = copy.deepcopy(board.board)
        if color == 2:
            Best_outcome = -Inf
            Best_move = None

            for action in self.getMoveList(state):
                print("Searching... : ", action)
                U = max(Best_outcome, self.minimax(self.result(state, action), d = self.depth)) 
                print(U)
                if U > Best_outcome:
                    Best_outcome = U
                    Best_move = action
            board.place(Best_move, color)
            ### TODO change below
            return(board.print()) ## In order to implement against another AI it has to actually return the board.
            
        elif color == 1:
            Best_outcome = Inf
            Best_move = None

            for action in self.getMoveList(state):
                print("Searching... : ", action)
                U = min(Best_outcome, self.minimax(self.result(state, action), d = self.depth)) 
                print(U)
                if U < Best_outcome:
                    Best_outcome = U
                    Best_move = action
            board.place(Best_move, color)
            return(board.print())