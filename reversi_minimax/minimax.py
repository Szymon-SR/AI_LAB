import argparse
import copy
import logging
import pickle
import time
from functools import cache

from reversi_minimax.game import (draw_board, get_score_of_board,
                                  get_valid_moves, make_move, who_won)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# 1 max
MAX_MAP = {True: 1, False: 2}


def possible_new_states(state, cur_player_index):
    valid_moves = get_valid_moves(state, cur_player_index)
    possible_states = []

    for x, y in valid_moves:
        copied_state = copy.deepcopy(state)
        make_move(copied_state, cur_player_index, x, y)
        possible_states.append(copied_state)

    return possible_states


def evaluate(state, is_maximizing):
    if get_valid_moves(state, MAX_MAP[is_maximizing]) == []:
        # game is over
        scores = get_score_of_board(state)
        if scores[1] == scores[2]:
            # draw
            return 0

        if scores[1] > scores[2]:
            # player 1 won over player 2
            return 1
            # TODO IDK
        else:
            return -1

def minimax(state, is_maximizing, alpha=-999, beta=999):
    if (score := evaluate(state, is_maximizing)) is not None:
        return score

    scores = []
    for new_state in possible_new_states(state, MAX_MAP[is_maximizing]):
        scores.append(score := minimax(new_state, not is_maximizing, alpha, beta))
        if is_maximizing:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)
        if beta <= alpha:
            break
    return (max if is_maximizing else min)(scores)


def solve(state):
    is_maximizing = True
    no_of_rounds = 0

    while get_valid_moves(state, MAX_MAP[is_maximizing]) != []:
        logger.info(f"Round {no_of_rounds}")
        move = generate_best_move(state, is_maximizing)
        state = move[1]
        is_maximizing = not is_maximizing
        no_of_rounds += 1

    draw_board(state)
    logger.info(who_won(state))
    logger.info(f"Number of rounds is {no_of_rounds}")


def generate_best_move(state, is_maximizing):
    if is_maximizing:
        return max(
            (minimax(new_state, is_maximizing=is_maximizing), new_state)
            for new_state in possible_new_states(state, 1)
        )
    else:
        return min(
            (minimax(new_state, is_maximizing=is_maximizing), new_state)
            for new_state in possible_new_states(state, 2)
        )


def best_move_for_max(state):
    return max(
        (minimax(new_state, is_maximizing=False), new_state)
        for new_state in possible_new_states(state, 2)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Solver of game states.")
    parser.add_argument("state_index")
    args = parser.parse_args()

    # load example game states from serialized file
    with open("reversi_minimax/game_states.pickle", "rb") as handle:
        states = pickle.load(handle)

    game_state = states[int(args.state_index)]

    logger.info("Chosen beginning state:")
    draw_board(game_state)
    logger.info("Result:")

    begin_run_time = time.time()
    result = solve(game_state)
    processing_time = time.time() - begin_run_time

    logger.info(f"Processing time - {processing_time}")