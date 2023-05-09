import logging

import numpy as np

import reversi_minimax.heuristics as heur

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

AI_PLAYERS = {
    # percentages show how important is each heuristic
    "Randomizer": {heur.heur_random: 100},
    "Avoid Corner": {heur.heur_avoid_corners: 100},
    "Edge and Corner": {heur.heur_edges: 50, heur.heur_corners: 50},
    "Center and Corner": {heur.heur_centralize: 25, heur.heur_corners: 75},
    "Proportion and Edge": {heur.heur_proportion_of_tiles: 40, heur.heur_edges: 60},
    "Center and Edge": {heur.heur_centralize: 25, heur.heur_edges: 75},
    "Corner Priority": {
        heur.heur_corners: 80,
        heur.heur_edges: 10,
        heur.heur_proportion_of_tiles: 10,
    },
}


def evaluate_by_strategy(state: list, strategies: dict):
    # Calculate weighted average from strategy parameters
    results = []
    weights = []

    for heuristic, weight in strategies.items():
        weights.append(weight)
        results.append(heuristic(state))

    logger.debug("results: " + str(results))
    logger.debug("weights " + str(weights))

    av = np.average(results, weights=weights)

    return av
