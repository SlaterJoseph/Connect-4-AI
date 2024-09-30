from typing import Callable

from Game.board import Board


class Agent:
    """
    An agent which will make Connect 4 moves against an opponent
    """

    def __init__(self, depth: int, eval_fn: Callable, search_fn: Callable):
        """
        Initializes the agent

        :param depth: The max depth that will be searched
        :param eval_fn: The evaluation function which will be used
        :param search_fn: The search function which will be used
        """
        self.depth = depth
        self.eval_fn = eval_fn
        self.search_fn = search_fn


    def move(self, game: Board, time_remaining) -> tuple:
        """
        A function calling the agent to make a move

        :param game: The game state
        :param time_remaining: The amount of time the agent has to search
        :return: The best found move
        """
        best_move, utility = self.search_fn(self, game, time_remaining, self.depth)
        return best_move

    def utility(self, game: Board) -> float:
        """
        A function which evaluates a game state

        :param game: The game state
        :return: A evaluation of the game state
        """
        return self.eval_fn(game)


