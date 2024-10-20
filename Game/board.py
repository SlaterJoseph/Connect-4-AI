import numpy as np
from Game.player import Player


class Board:
    def __init__(self, player_1: Player, player_2: Player):
        """
        Initialize our game
        player_1: The first player
        player_2: The second player
        """
        self.rows = 6
        self.cols = 7
        self.size = 0

        self.board = np.zeros((self.rows, self.cols))

        self.player_1 = player_1
        self.player_2 = player_2

        self.possible_actions = [x for x in range(0, 7)]
        self.player_1_turn = True

    def __str__(self) -> str:
        """
        A function which prints out the board
        :return: A string format of the board
        """
        string_board = '\n'.join([' | '.join(map(str, row)) for row in self.board])
        return string_board

    def copy(self):
        """
        Gives a copy of the current board state

        :return: A copy of the board state
        """
        board = Board(self.player_1, self.player_2)
        board.size = self.size
        board.board = self.board
        board.possible_actions = self.possible_actions
        return board

    def forecast_move(self, move: int, player: Player) -> tuple:
        """
        Creates a copy of the board with a new move being played

        :param move: The move to apply
        :param player: The player making the move
        :return: A copy of the board, result of the action
        """
        new_game = self.copy()
        result = new_game.drop(move, player)
        return new_game, result

    def col_full(self, col: int) -> bool:
        """
        Checks if a column is full

        :param col: The column to check
        :return: boolean indicate if the column is full
        """
        if self.board[0][col] != 0:
            return True
        return False

    def drop(self, col: int, player: Player) -> int:
        """
        Drop the piece
        :param col: The column to drop the piece in
        :param player: The player making the move
        :return: An integer representing the termination state
            0 - Ongoing
            1 - Winner Found
            2 - Draw
        """
        row = np.max(np.where(self.board[:, col] == 0))
        if row == 5:
            self.possible_actions.remove(col)

        if player == self.player_1:
            self.board[row][col] = 1
        else:
            self.board[row][col] = 2

        self.player_1_turn = not self.player_1_turn
        winner = self.terminate(row, col)

        terminate = 1 if winner else 2 if self.size == 42 else 0
        return terminate

    def terminate(self, x, y) -> bool:
        """
        Checks if the current player has won
        :param x: The row of the new move
        :param y: The col of the new move
        :return: A boolean indicating if a winner was found
        """

        def across():  # Row check
            row = self.board[x]
            for loc in range(3, 7):
                if np.all(row[loc: loc + 4] == row[loc]) and row[loc] != 0:
                    return True
            return False


        def up():  # Col check
            col = self.board[:, y]
            for start in range(len(col) - 3):
                if np.all(col[start:start + 4] == col[start]) and col[start] != 0:
                    return True
            return False

        def diagonal_1():  # 0,0 to 5,6
            diag = np.diagonal(self.board, offset=(y - x))
            for start in range(len(diag) - 3):
                if np.all(diag[start:start + 4] == diag[start]) and diag[start] != 0:
                    return True
            return False

        def diagonal_2():  # 0,6 to 5,0
            flipped_board = np.fliplr(self.board)
            anti_diag = np.diagonal(flipped_board, offset=(y - (5 - x)))
            for start in range(len(anti_diag) - 3):
                if np.all(anti_diag[start:start + 4] == anti_diag[start]) and anti_diag[start] != 0:
                    return True
            return False

        if across() or up() or diagonal_1() or diagonal_2():
            return True
        else:
            return False

    def get_actions(self) -> list:
        """
        Returns our possible actions

        :return: A list of the actions
        """
        return self.possible_actions

    def get_game(self) -> list:
        """
        Return our game state

        :return: board
        """
        return self.board

    def get_turn(self) -> bool:
        """
        Returns True if it is player 1's turn
        :return: boolean indicating whose turn it is
        """
        return self.player_1_turn

    def possible_wins_remaining(self) -> tuple:
        """
        Checks for all possible wins of each player
        :return: A tuple of players possible win, opponents possible wins
        """

        if self.player_1_turn:
            turn_of = 1
            opp = 2
        else:
            turn_of = 2
            opp = 1

        player_wins = 0
        opponent_wins = 0

        def check_windows(windows, target):
            return np.sum(np.all((windows == target) | (windows == 0), axis=1))

        # Row checks
        for r in range(self.rows):
            row_windows = np.lib.stride_tricks.sliding_window_view(self.board[r], window_shape=4)
            player_wins += check_windows(row_windows, turn_of)
            opponent_wins += check_windows(row_windows, opp)

        # Column checks
        for c in range(self.cols):
            col_windows = np.lib.stride_tricks.sliding_window_view(self.board[:, c], window_shape=4)
            player_wins += check_windows(col_windows, turn_of)
            opponent_wins += check_windows(col_windows, opp)

        # Diagonal checks (top-left to bottom-right)
        for offset in range(-self.rows + 4, self.cols - 3):
            diagonal = np.diagonal(self.board, offset=offset)
            if len(diagonal) >= 4:
                diag_windows = np.lib.stride_tricks.sliding_window_view(diagonal, window_shape=4)
                player_wins += check_windows(diag_windows, turn_of)
                opponent_wins += check_windows(diag_windows, opp)

        # Diagonal checks (top-right to bottom-left)
        flipped_board = np.fliplr(self.board)
        for offset in range(-self.rows + 4, self.cols - 3):
            anti_diagonal = np.diagonal(flipped_board, offset=offset)
            if len(anti_diagonal) >= 4:
                anti_diag_windows = np.lib.stride_tricks.sliding_window_view(anti_diagonal, window_shape=4)
                player_wins += check_windows(anti_diag_windows, turn_of)
                opponent_wins += check_windows(anti_diag_windows, opp)

        return player_wins, opponent_wins
