import argparse
import logging
import pickle
import time

from reversi_minimax.game import draw_board
from reversi_minimax.minimax import best_move_for_max

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
    move = best_move_for_max(game_state)
    processing_time = time.time() - begin_run_time

    logger.info(move[0])
    draw_board(move[1])
    logger.info(f"Processing time - {processing_time}")
