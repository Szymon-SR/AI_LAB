from abc import ABC
from datetime import time

class BusStop:
    def __init__(self) -> None:
        pass

class BaseSolution(ABC):
    def __init__(self, source: BusStop, destination: BusStop, optimize_by: str, starting_time: time) -> None:
        pass

class DijkstraSolution(BaseSolution):
    pass

class AStarSolution(BaseSolution):
    pass
