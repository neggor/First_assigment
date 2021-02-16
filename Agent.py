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
    
    def Dijkstra(self, state):
        TMP_board = HexBoard(self.size)
        TMP_board.board = state
        #TODO
        #For red player
        univisted_set = set([x for x in state if state[x] != 1]) ## Unvisited are reds an empty

        for initial in [x for x in univisted_set if x[0] == 0]:
            for end in [x for x in univisted_set if x[1] == self.size - 1]: # All possible initial and end points
                cost = 0
                current_univisited_set = copy.deepcopy(univisted_set)
                current = initial
                objective = end





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
                #TODO
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
        
    def MakeMove(self, board, color): # Make a move using AI
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
            return(board.print())
        
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