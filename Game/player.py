from typing import Callable
from Agents.agent import Agent
from Agents.base_minimax import minimax
from Agents.heuristics import possible_wins, weighted_possible_wins


class Player:
    def __init__(self, agent: int = None) -> None:
        self.board = None

        if agent is None:
            self.human = True
            self.agent = None
        else:
            self.human = False
            self.agent = self.define_agent(agent)

    def turn(self) -> int:
        """
        Calls the proper outlet for getting the new move
        :return: The column which the piece will be dropped into
        """
        if self.human:
            col = int(input('Please choose a column to drop a piece in: '))
        else:
            col = self.agent.move()

        return col

    def update_board(self, board: list) -> None:
        """
        Update the board
        :param board: The game state of the board
        :return: None
        """
        self.board = board

    def define_agent(self, marker: int) -> Callable or None:
        """
        Returns the proper function for the agent
        :param marker: The marker to indicate what algorithm to return
        :return: An algorithm (function)
        """
        if marker == 1:
            return Agent(5, possible_wins, minimax)
        else:
            return None