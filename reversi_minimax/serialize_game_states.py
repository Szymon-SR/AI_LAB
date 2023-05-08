import pickle

EXAMPLE_GAMESTATES = [
    [
        [0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 2, 1, 0, 0],
        [0, 0, 0, 2, 1, 2, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 1, 2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
        [0, 0, 0, 2, 2, 0, 0, 2],
        [0, 0, 0, 2, 2, 0, 2, 0],
        [0, 0, 2, 2, 2, 2, 0, 0],
        [0, 0, 2, 1, 1, 0, 0, 0],
        [0, 0, 2, 1, 1, 1, 0, 0],
        [0, 2, 2, 2, 1, 1, 0, 0],
        [2, 1, 2, 1, 2, 1, 0, 0],
        [1, 2, 0, 2, 0, 2, 0, 0],
    ],
    [
        [1, 1, 2, 0, 0, 1, 0, 2],
        [1, 1, 1, 2, 0, 1, 2, 0],
        [1, 2, 2, 2, 2, 1, 2, 0],
        [1, 1, 2, 2, 2, 2, 2, 0],
        [1, 1, 1, 1, 1, 2, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 1, 1, 2, 1, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
    ],
]

# Serialize arbitrary example game states to file, for later usage
if __name__ == "__main__":
    with open("reversi_minimax/game_states.pickle", "wb") as handle:
        pickle.dump(EXAMPLE_GAMESTATES, handle, protocol=pickle.HIGHEST_PROTOCOL)