import logging
import pickle

from reversi_minimax.game import draw_board, get_valid_moves

STATE_INDEX = 1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    with open("reversi_minimax/game_states.pickle", "rb") as handle:
        states = pickle.load(handle)

    game_state = states[STATE_INDEX]

    # Valid moves
    draw_board(game_state)
    # valid moves returns coordinates starting from 0 index,
    # while draw board draws from 1
    logger.info(get_valid_moves(game_state, 1))
    logger.info(get_valid_moves(game_state, 2))
