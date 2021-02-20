from Agent import AGENT
from hex_skeleton import HexBoard
from trueskill import rate_1vs1

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
    turn += 1
    play(Blue_player, Red_player, new_board, turn = turn) ## Call another turn
    
def main():
    board_size = 3
    # Player 1, depth = 3 and random heuristic:
    Player_one = AGENT(board_size = board_size, depth = 3, Dijkstra = False)
    # Plater 2, depth = 3 and Dijkstra heuristic:
    Player_two = AGENT(board_size = board_size, depth = 3, Dijkstra = True)
    # Plater 3, depth = 4 and Dijkstra heuristic:
    Player_three = AGENT(board_size = board_size, depth = 4, Dijkstra = True)

    Blue_player = Player_two
    Red_player = Player_three
    THE_board = HexBoard(board_size)
    play(Blue_player, Red_player, THE_board)

if __name__ == '__main__':
    main()
