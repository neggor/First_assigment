from hex_skeleton import HexBoard
from numpy.core.numeric import Inf
import itertools, re, sys, random
import copy
import pdb
class AGENT:

    def __init__(self, board_size, depth, Dijkstra = False):
        self.size = board_size
        self.depth = depth
        self.Dijkstra = Dijkstra
        self.cutoffs = 0
        self.nodos = 0
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

    def generate_graph(self, state, color):
        TMP_board = HexBoard(self.size)
        TMP_board.board = state
        available = [x for x in state if (state[x] == 3 or state[x] == color)]
        costs = {}
        graph = {}
        available_clean = copy.deepcopy(available)
        for node in available:
            # Assing values:
            if TMP_board.board[node] == color:
                costs[node] = 0
            else:
                costs[node] = 1

            # Not include isolated nodes in the graph:
            if all([(TMP_board.board[x]!= color and TMP_board.board[x] != 3) for x in TMP_board.get_neighbors(node)]):
                continue 

            graph[node] = ({}, costs[node])

        for node in available_clean:
            for neighbour in [x for x in TMP_board.get_neighbors(node) if ((TMP_board.board[x] == color or TMP_board.board[x] == 3) and x in costs)]:
                    graph[node][0].update({neighbour:costs[neighbour]})
        return(graph)

    def shortest_path(self, graph, initial, end, state, distance = {}, visited = [], predecessor = {}):
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
            distance[initial] = graph[initial][1]
            visited.append(initial)
            for neighbour in graph[initial][0]:
                if neighbour not in visited:
                    new_distance = distance[initial] + graph[initial][0][neighbour]
                    
                    if new_distance < distance.get(neighbour, Inf):
                        distance[neighbour] = new_distance
                        predecessor[neighbour] = initial
            unvisited = {}
            for node in graph:
                if node not in visited:
                    unvisited[node] = distance.get(node, Inf)
            next = min(unvisited, key = unvisited.get)
            length = self.shortest_path(graph, next, end, state, distance, visited, predecessor)
            return(length)
    
    def Dijkstra_heuristic(self, state):
        TMP_board = HexBoard(self.size)
        TMP_board.board = copy.deepcopy(state)
        univisted_set = set([x for x in state if state[x] != 1]) 
        min_distance_red = Inf
        for initial in [x for x in univisted_set if x[1] == 0]:
            for end in [x for x in univisted_set if x[1] == self.size - 1]:
                distance = {}
                visited = []
                predecessor = {} 
                distance_red = self.shortest_path(self.generate_graph(state, 2), initial, end, state, distance, visited, predecessor)
                if distance_red < min_distance_red:
                    min_distance_red = distance_red
        univisted_set = set([x for x in state if state[x] != 2]) 
        min_distance_blue = Inf
        for initial in [x for x in univisted_set if x[0] == 0]:
            for end in [x for x in univisted_set if x[0] == self.size - 1]: 
                distance = {}
                visited = []
                predecessor = {}
                distance_blue = self.shortest_path(self.generate_graph(state, 1), initial, end, state, distance, visited, predecessor)
                if distance_blue < min_distance_blue:
                    min_distance_blue = distance_blue

        if sum([TMP_board.is_color(x, 1) for x in TMP_board.board]) >= \
                sum([TMP_board.is_color(x, 2) for x in TMP_board.board]):
            heuristic_value = min_distance_blue
        else:
            heuristic_value = -min_distance_red

        return(heuristic_value)
                    
    def eval(self, state):
        TMP_board = HexBoard(self.size)
        TMP_board.board = state
        if TMP_board.check_win(2) or TMP_board.check_win(1) or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0:
            if TMP_board.check_win(2):
                return(100)
            elif TMP_board.check_win(1):
                return(-100)
            else:
                return(0)
        else:
            if self.Dijkstra:
                value = self.Dijkstra_heuristic(state)
                return(value)

            else:
                return(random.uniform(-1,1))

    def minimax(self, state, d, alpha = -Inf, beta = Inf): # Returns the value of the LEAF following optimal play for both players 
        TMP_board = HexBoard(self.size)
        TMP_board.board = state
        if d <= 0:
            return(self.eval(state))
        else:
            if sum([TMP_board.is_color(x, 1) for x in TMP_board.board]) >= \
                    sum([TMP_board.is_color(x, 2) for x in TMP_board.board]): 
                value = -Inf  
                if TMP_board.check_win(2) or TMP_board.check_win(1) or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0: 
                    return(self.eval(state))
                else:
                    for action in self.getMoveList(state): 
                        self.nodos += 1
                        value = max(value, self.minimax(self.result(state, action), d-1, alpha, beta))
                        alpha = max(value, alpha)
                        if alpha >= beta:
                            self.cutoffs += 1 
                            break
                    return(value)
            else:
                value = Inf 
                if TMP_board.check_win(2) or TMP_board.check_win(1) or sum([TMP_board.is_empty(x) for x in TMP_board.board]) == 0: 
                    return(self.eval(state))   
                else:
                    for action in self.getMoveList(state):
                        self.nodos += 1
                        value = min(value, self.minimax(self.result(state, action), d-1, alpha, beta))
                        beta = min(value, beta)
                        if alpha >= beta:
                            self.cutoffs += 1 
                            break
                    return(value)
        
    def MakeMove(self, board, color):
        state = copy.deepcopy(board.board)
        if color == 2:
            Best_outcome = -Inf
            Best_move = None

            for action in self.getMoveList(state):
                prevc = self.cutoffs ## Those two prev are just to print the increment for each action
                prevn = self.nodos
                print("Searching... : ", action)
                U = max(Best_outcome, self.minimax(self.result(state, action), d = self.depth)) 
                print("Value:", U)
                print("Cutoffs:", self.cutoffs - prevc)
                print("Searched nodes:", self.nodos - prevn)
                if U > Best_outcome:
                    Best_outcome = U
                    Best_move = action
            board.place(Best_move, color)
            board.print()
            return(board)
            
        elif color == 1:
            Best_outcome = Inf
            Best_move = None

            for action in self.getMoveList(state):
                prevc = self.cutoffs ## Those two prev are just to print the increment for each action
                prevn = self.nodos
                print("Searching... : ", action)
                U = min(Best_outcome, self.minimax(self.result(state, action), d = self.depth)) 
                print("Value:", U)
                print("Cutoffs:", self.cutoffs - prevc)
                print("Searched nodes:", self.nodos - prevn)
                if U < Best_outcome:
                    Best_outcome = U
                    Best_move = action
            board.place(Best_move, color)
            board.print()
            return(board)