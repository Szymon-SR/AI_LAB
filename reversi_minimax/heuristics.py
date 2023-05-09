import random

from reversi_minimax.constants import MAX_MAP
from reversi_minimax.game import get_score_of_board


def fit_range(value):
    if value > 1:
        return 1
    elif value < -1:
        return -1
    else:
        return value


def heur_random(_):
    # used as a benchmark
    return random.random() * 2 - 1


def heur_proportion_of_tiles(state):
    # based on number of tiles each player has

    scores = get_score_of_board(state)
    proportion = (scores[MAX_MAP[True]] / scores[MAX_MAP[False]]) - 1
    print(fit_range(proportion))
    return fit_range(proportion)


def heur_corners(state):
    # based on number of corner tiles

    corner_tiles = [
        state[0][0],
        state[0][7],
        state[7][0],
        state[7][7],
    ]
    num_of_corners = 0
    for corner in corner_tiles:
        if corner == MAX_MAP[True]:
            num_of_corners += 1
        if corner == MAX_MAP[False]:
            num_of_corners -= 1

    return num_of_corners * 0.25  # this way all 4 corners for max means 1,
    # and all 4 corners for min means -1, equal to total win

def heur_avoid_corners(state):
    # benchmark, should be losing

    corner_tiles = [
        state[0][0],
        state[0][7],
        state[7][0],
        state[7][7],
    ]
    num_of_corners = 0
    for corner in corner_tiles:
        if corner == MAX_MAP[True]:
            num_of_corners += 1
        if corner == MAX_MAP[False]:
            num_of_corners -= 1

    return -(num_of_corners * 0.25)  # this way all 4 corners for max means 1,
    # and all 4 corners for min means -1, equal to total win

def heur_centralize(state):
    # gives preference to centrally positioned tiles
    
    # this list stores the value of row/column, middle columns
    # such as 4, 5 are worth the most
    index_values = [0.1, 0.1, 0.2, 0.5, 0.5, 0.2, 0.1, 0.1]

    max_evaluation = 0
    min_evaluation = 0

    for row_id, row in enumerate(state):
        for col_id, tile in enumerate(row):
            if tile == MAX_MAP[True]:
                max_evaluation += index_values[row_id]
                max_evaluation += index_values[col_id]
            elif tile == MAX_MAP[False]:
                min_evaluation += index_values[row_id]
                min_evaluation += index_values[col_id]

    evaluation = (max_evaluation / min_evaluation) - 1
    print(evaluation)
    return fit_range(evaluation)


def heur_edges(state):
    # gives preference to edges
    max_evaluation = 1
    min_evaluation = 1

    edge_ids = (0, 7)

    for row_id, row in enumerate(state):
        for col_id, tile in enumerate(row):
            if row_id in edge_ids or col_id in edge_ids:
                if tile == MAX_MAP[True]:
                    max_evaluation += 1
                if tile == MAX_MAP[False]:
                    min_evaluation += 1

    evaluation = (max_evaluation / min_evaluation) - 1
    print(evaluation)
    return fit_range(evaluation)