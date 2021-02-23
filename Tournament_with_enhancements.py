from Agent import AGENT, Agent_with_enhancements
from hex_skeleton import HexBoard
import itertools
import trueskill
import random
import matplotlib.pyplot as plt

def play(Blue_player, Red_player, board, turn = 0):
    if board.is_game_over():
        if board.check_win(1):
            print("Blue wins")
            return(1)
        if board.check_win(2):
            print("Red wins")
            return(2)
        else:
            print("Stalemate")
            return(0)

    if sum([board.is_color(x, 1) for x in board.board]) == sum([board.is_color(x, 2) for x in board.board]):
        new_board = Red_player.MakeMove(board, 2) # Update board
    else:
        new_board = Blue_player.MakeMove(board, 1) # Update board
    print("Turn:", turn)
    board.print()
    turn += 1
    return(play(Blue_player, Red_player, new_board, turn = turn)) ## Call another turn

    
def main():
    board_size = 4
    # Player 1, depth = 3 and random heuristic:
    Player_0 = AGENT(board_size = board_size, depth = 2, Dijkstra = False)
    r0 = trueskill.Rating()
    # Player 2, depth = 3 and Dijkstra heuristic:
    Player_1 = AGENT(board_size = board_size, depth = 2, Dijkstra = True)
    r1 = trueskill.Rating()
    # Player 3, depth = 4 and Dijkstra heuristic:
    Player_2 = AGENT(board_size = board_size, depth = 3, Dijkstra = True)
    r2 = trueskill.Rating()
    # Player 4, think time = 10 secs
    Player_3 = Agent_with_enhancements(board_size = board_size)
    r3 = trueskill.Rating()
    
    players = {"player 0": r0, "player 1": r1, "player 2" : r2, "player 3" : r3}
    possible_matches = list(itertools.permutations(("player 0", "player 1", "player 2", "player 3"), r = 2))
    result = {}
    play_n = 0
    s_mu = [players["player 0"].mu, players["player 1"].mu, players["player 2"].mu, players["player 3"].mu]
    s_mu_new = [0, 0, 0, 0]
    Player_0_elo = []
    Player_1_elo = []
    Player_2_elo = []
    Player_3_elo = []
    while play_n < 30:
        random.shuffle(possible_matches)
        for match in possible_matches:
            print(match)
            THE_board = HexBoard(board_size)
            play_n += 1
            # Red player
            if match[0] == "player 0":
                Red_player = Player_0
            if match[0] == "player 1":
                Red_player = Player_1
            if match[0] == "player 2":
                Red_player = Player_2
            if match[0] == "player 3":
                Red_player = Player_3
            # Blue player
            if match[1] == "player 0":
                Blue_player = Player_0
            if match[1] == "player 1":
                Blue_player = Player_1
            if match[1] == "player 2":
                Blue_player = Player_2
            if match[1] == "player 3":
                Blue_player = Player_3

            result[play_n] = play(Blue_player, Red_player, THE_board)
            
            if result[play_n] == 1: # Blue wins
                players[match[1]], players[match[0]] = trueskill.rate_1vs1(players[match[1]], players[match[0]])
            elif result[play_n] == 2: # Red wins
                players[match[0]] , players[ match[1]] = trueskill.rate_1vs1(players[match[0]], players[ match[1]])
            else:
                players[match[0]] , players[match[1]] = trueskill.rate_1vs1( players[match[0]], players[match[1]], drawn = True)

            s_mu_new = [players["player 0"].mu, players["player 1"].mu, players["player 2"].mu,  players["player 3"].mu]

            Player_0_elo.append(players["player 0"].mu)
            Player_1_elo.append(players["player 1"].mu)
            Player_2_elo.append(players["player 2"].mu)
            Player_3_elo.append(players["player 3"].mu)
            
    for index, player in enumerate([Player_0_elo, Player_1_elo, Player_2_elo, Player_3_elo]):
        plt.plot(player, label = "player %s" %index)
        plt.legend()
    plt.show()

    print(play_n)
    print(players)

    data = {"P0": (Player_0.nodos/play_n, Player_0.cutoffs/play_n),\
        "P1": ((Player_1.nodos/play_n, Player_1.cutoffs/play_n)) ,\
            " P2": ((Player_2.nodos/play_n, Player_2.cutoffs/play_n)),\
                "P3": ((Player_3.nodos/play_n, Player_3.cutoffs/play_n))}
    print(data)

if __name__ == '__main__':
    main()
