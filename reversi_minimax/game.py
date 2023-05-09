import copy
import random
import sys

from termcolor import colored

from reversi_minimax.constants import BOARD_SIZE


def create_board():
    # Returns a board / game state
    board = []
    for i in range(BOARD_SIZE):
        board.append([0] * BOARD_SIZE)

    board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    board[4][4] = 1

    return board


def who_won(state: list):
    score = get_score_of_board(state)
    if score[1] > score[2]:
        return f"Player one won {score[1]} vs {score[2]}"
    elif score[1] == score[2]:
        return f"Game ended in a draw {score[1]} vs {score[2]}"
    else:
        return f"Player two won {score[2]} vs {score[1]}"


def draw_board(state: list):
    # print for purpose of generating test cases
    print(colored(state, "red"))

    HLINE = "  ---------------------------------"
    VLINE = "  |   |   |   |   |   |   |   |   |"

    print(colored("    1   2   3   4   5   6   7   8", "green"))
    print(colored(HLINE, "green"))
    for y in range(BOARD_SIZE):
        print(colored(VLINE, "green"))
        print(colored(y + 1, "green"), end=" ")
        for x in range(BOARD_SIZE):
            to_print = state[x][y]

            if state[x][y] == 0:
                to_print = " "

            print(colored("| %s" % (to_print), "green"), end=" ")
        print(colored("|", "green"))
        print(colored(VLINE, "green"))
        print(colored(HLINE, "green"))


def is_valid_move(state: list, player_number: int, xstart: int, ystart: int):
    if state[xstart][ystart] != 0 or not is_on_board(xstart, ystart):
        return False

    state[xstart][ystart] = player_number  # temporarily set the tile on the board.

    other_tile = 1 if player_number == 2 else 2

    tiles_to_flip = []
    for xdirection, ydirection in [
        [0, 1],
        [1, 1],
        [1, 0],
        [1, -1],
        [0, -1],
        [-1, -1],
        [-1, 0],
        [-1, 1],
    ]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if is_on_board(x, y) and state[x][y] == other_tile:
            # Enemy piece
            x += xdirection
            y += ydirection
            if not is_on_board(x, y):
                continue
            while state[x][y] == other_tile:
                x += xdirection
                y += ydirection
                if not is_on_board(x, y):
                    break
            if not is_on_board(x, y):
                continue
            if state[x][y] == player_number:
                # Check how many tiles can be taken
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tiles_to_flip.append([x, y])

    # Fix board
    state[xstart][ystart] = 0
    if len(tiles_to_flip) == 0:
        # invalid
        return False
    return tiles_to_flip


def is_on_board(x: int, y: int):
    return x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE


def get_valid_moves(state: list, player_number: int):
    valid_moves = []

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if is_valid_move(state, player_number, x, y):
                valid_moves.append([x, y])
    # print(colored(tile, 'yellow'))

    # print(colored(validMoves, 'red'))
    return valid_moves


def get_score_of_board(state: list):
    player1_score = 0
    player2_score = 0
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if state[x][y] == 1:
                player1_score += 1
            if state[x][y] == 2:
                player2_score += 1
    return {1: player1_score, 2: player2_score}


def enter_player_tile():
    tile = 0
    while not (int(tile) in (1, 2)):
        print("Pick 1 or 2")
        tile = input().upper()

    if int(tile) == 1:
        return [1, 2]
    else:
        return [2, 1]


def who_goes_first():
    # used for testing games
    if random.randint(0, 1) == 0:
        return "computer"
    else:
        return "player"


def make_move(state: list, player_number: int, xstart: int, ystart: int):
    tiles_to_flip = is_valid_move(state, player_number, xstart, ystart)

    if not tiles_to_flip:
        return False

    state[xstart][ystart] = player_number
    for x, y in tiles_to_flip:
        state[x][y] = player_number
    return True


def is_on_corner(x: int, y: int):
    return (
        (x == 0 and y == 0)
        or (x == (BOARD_SIZE - 1) and y == 0)
        or (x == 0 and y == (BOARD_SIZE - 1))
        or (x == (BOARD_SIZE - 1) and y == (BOARD_SIZE - 1))
    )


def get_player_move(state: list, player_number: int):
    # used for testing games

    DIGITS1TO8 = "1 2 3 4 5 6 7 8".split()
    while True:
        print("Enter your move, or type quit to end the game")
        move = input().lower()
        if move == "quit":
            return "quit"

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if not is_valid_move(state, player_number, x, y):
                continue
            else:
                break
        else:
            print(
                "That is not a valid move. Type the x digit (1-8), then the y digit (1-8)."
            )
            print("For example, 81 will be the top-right corner.")

    return [x, y]


def get_computer_move(state: list, computer_number: int):
    # simple computer (not minimax) to generate test cases
    possible_moves = get_valid_moves(state, computer_number)

    random.shuffle(possible_moves)

    for x, y in possible_moves:
        if is_on_corner(x, y):
            return [x, y]

    best_score = -1
    for x, y in possible_moves:
        copied_board = copy.deepcopy(state)
        make_move(copied_board, computer_number, x, y)
        score = get_score_of_board(copied_board)[computer_number]
        if score > best_score:
            best_move = [x, y]
            best_score = score
    return best_move


def show_points(player_number: int, computer_number: int):
    scores = get_score_of_board(main_board)
    print(
        "You have %s points. The computer has %s points."
        % (scores[player_number], scores[computer_number])
    )


if __name__ == "__main__":
    while True:
        main_board = create_board()
        player_tile, computer_tile = enter_player_tile()
        turn = who_goes_first()
        print("The " + turn + " will go first.")

        while True:
            if turn == "player":
                draw_board(main_board)
                show_points(player_tile, computer_tile)
                move = get_player_move(main_board, player_tile)
                if move == "quit":
                    sys.exit()
                else:
                    make_move(main_board, player_tile, move[0], move[1])

                if get_valid_moves(main_board, computer_tile) == []:
                    break
                else:
                    turn = "computer"

            else:
                draw_board(main_board)
                show_points(player_tile, computer_tile)
                input("Press Enter to see the computer's move.")
                x, y = get_computer_move(main_board, computer_tile)
                make_move(main_board, computer_tile, x, y)

                if get_valid_moves(main_board, player_tile) == []:
                    break
                else:
                    turn = "player"

        draw_board(main_board)
        scores = get_score_of_board(main_board)
        print(
            "Player 1 scored %s points. Player 2 scored %s points."
            % (scores[1], scores[2])
        )
        if scores[player_tile] > scores[computer_tile]:
            print(
                "You beat the computer by %s points! Congratulations!"
                % (scores[player_tile] - scores[computer_tile])
            )
        elif scores[player_tile] < scores[computer_tile]:
            print(
                "You lost. The computer beat you by %s points."
                % (scores[computer_tile] - scores[player_tile])
            )
        else:
            print("The game was a tie!")

        break
