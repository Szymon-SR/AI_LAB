import argparse
import logging
import pickle
import time

from termcolor import colored

from reversi_minimax.constants import PLAYER_ID_MAP
from reversi_minimax.game import draw_board, get_score_of_board
from reversi_minimax.minimax import generate_best_move

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Solver of game states.")
    parser.add_argument("state_index")
    parser.add_argument("id")
    args = parser.parse_args()

    # load example game states from serialized file
    with open("reversi_minimax/game_states.pickle", "rb") as handle:
        states = pickle.load(handle)

    game_state = states[int(args.state_index)]

    logger.info("Chosen beginning state:")
    draw_board(game_state)
    logger.info("Result:")

    begin_run_time = time.time()
    move = generate_best_move(game_state, PLAYER_ID_MAP[int(args.id)])
    processing_time = time.time() - begin_run_time

    logger.info(colored(move[0], "yellow"))
    draw_board(move[1])
    logger.info(get_score_of_board(move[1]))
    logger.info(f"Processing time - {processing_time}")
