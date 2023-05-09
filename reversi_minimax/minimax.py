import argparse
import copy
import logging
import pickle
import time
from functools import cache

import reversi_minimax.heuristics as heur
from reversi_minimax.constants import DEPTH_LIMIT, MAX_MAP
from reversi_minimax.game import (draw_board, get_score_of_board,
                                  get_valid_moves, make_move, who_won)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# 1 max


def possible_new_states(state, cur_player_index):
    valid_moves = get_valid_moves(state, cur_player_index)
    possible_states = []

    for x, y in valid_moves:
        copied_state = copy.deepcopy(state)
        make_move(copied_state, cur_player_index, x, y)
        possible_states.append(copied_state)

    return possible_states


def evaluate(state, is_maximizing, depth, heuristic):
    # return some value if either game is over, or depth limit reached

    if get_valid_moves(state, MAX_MAP[is_maximizing]) == []:
        # game is over - return "binary" score
        scores = get_score_of_board(state)
        if scores[1] == scores[2]:
            # draw
            return 0

        if scores[1] > scores[2]:
            # player 1 won over player 2
            return 1
        else:
            return -1

    if depth == 0:
        # depth limit was reached - return heuristic based score
        logger.info("Depth limit reached, calculating heuristic")
        return heuristic(state)


def minimax(state, is_maximizing, depth, alpha=-999, beta=999):

    if is_maximizing:
        # player two heur
        if (score := evaluate(state, is_maximizing, depth, heur.heur_corners)) is not None:
            return score
    else:
        # player one heur
        if (score := evaluate(state, is_maximizing, depth, heur.heur_corners)) is not None:
            return score

    scores = []
    for new_state in possible_new_states(state, MAX_MAP[is_maximizing]):
        scores.append(
            score := minimax(new_state, not is_maximizing, depth - 1, alpha, beta)
        )
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

    # NO VALID MOVES = game is finished
    logger.info(f"Player {MAX_MAP[is_maximizing]} has no legal moves.")
    draw_board(state)
    logger.info(who_won(state))
    logger.info(f"Number of rounds is {no_of_rounds}")


def generate_best_move(state, is_maximizing):
    if is_maximizing:
        return max(
            (minimax(new_state, is_maximizing, DEPTH_LIMIT), new_state)
            for new_state in possible_new_states(state, 1)
        )
    else:
        return min(
            (minimax(new_state, is_maximizing, DEPTH_LIMIT), new_state)
            for new_state in possible_new_states(state, 2)
        )


def best_move_for_max(state):
    return max(
        (minimax(new_state, False, DEPTH_LIMIT), new_state)
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
