import argparse
import logging
import pickle

from reversi_minimax.game import draw_board, get_valid_moves

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Solver of game states.")
    parser.add_argument("state_index")
    args = parser.parse_args()

    with open("reversi_minimax/game_states.pickle", "rb") as handle:
        states = pickle.load(handle)

    game_state = states[int(args.state_index)]

    # Valid moves
    draw_board(game_state)
    # valid moves returns coordinates starting from 0 index,
    # while draw board draws from 1
    for i in range(1, 3):
        logger.info(f"Valid moves of player {i} are:")
        logger.info(get_valid_moves(game_state, i))
