class Board:
    def __init__(self, player_1, player_2):
        """
        Initialize our game
        player_1: The first player
        player_2: The second player
        """
        self.rows = 6
        self.cols = 7
        self.size = 0

        self.board = [[0 for _ in range(self.rows)] for _ in range(self.cols)]

        self.player_1 = player_1
        self.player_2 = player_2

    def copy(self):
        board = Board(self.player_1, self.player_2)
        board.size = self.size
        board.board = self.board
        return board

    def get_game(self) -> list:
        """
        Return our game state

        :return: board
        """
        return self.board

    def forecast_move(self, move, player) -> tuple:
        new_game = self.copy()
        result = new_game.drop(move, player)
        return new_game, result

    def col_full(self, col) -> bool:
        """
        Checks if a column is full

        :param col: The column to check
        :return: boolean indicate if the column is full
        """
        if self.board[0][col] != 0:
            return True
        return False

    def drop(self, col, player) -> int:
        """
        Drop the piece
        :param col: The column to drop the piece in
        :param player: The player making the move
        :return: An integer representing the termination state
            0 - Ongoing
            1 - Winner Found
            2 - Draw
        """

        # Finds the proper place to drop the piece into
        row = 5
        for x in range(5, -1, -1):
            if self.board[x][col] != 0:
                row = x + 1
                break

        if player == self.player_1:
            self.board[row][col] = 1
        else:
            self.board[row][col] = 2

        winner = self.terminate(row, col)

        if winner:
            terminate = 1
        elif not winner and self.size == 42:
            terminate = 2
        else:
            terminate = 0

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
                cell_1, cell_2, cell_3, cell_4 = row[loc - 3], row[loc - 2], row[loc - 1], row[loc]
                if cell_1 == cell_2 == cell_3 == cell_4 and cell_1 != 0:
                    return True
                return False

        def up():  # Col check
            for loc in range(3, 6):
                cell_1, cell_2, cell_3, cell_4 = (self.board[loc - 3][y],
                                                  self.board[loc - 2][y],
                                                  self.board[loc - 1][y],
                                                  self.board[loc][y])
                if cell_1 == cell_2 == cell_3 == cell_4 and cell_1 != 0:
                    return True
            return False

        def diagonal_1():  # 0,0 to 5,6
            chip = self.board[x][y]
            if chip == 0:  # Edge case
                return False

            x_down, y_down = x - 1, y - 1  # To top left corner
            count = 1
            while x_down > -1 and y_down > -1 and self.board[x_down][y_down] == chip:
                count += 1
                x_down -= 1
                y_down -= 1

            x_up, y_up = x + 1, y + 1  # To bottom right corner
            while x_up < 6 and y_up < 7 and self.board[x_up][y_up] == chip:
                count += 1
                x_up += 1
                y_up += 1

            return count >= 4

        def diagonal_2():  # 0,6 to 5,0
            chip = self.board[x][y]
            if chip == 0:  # edge case
                return False

            x_down, y_up = x - 1, y + 1  # To top left corner
            count = 1
            while x_down > -1 and y_up < 7 and self.board[x_down][y_up] == chip:
                count += 1
                x_down -= 1
                y_up += 1

            x_up, y_down = x + 1, y - 1  # To bottom right corner
            while x_up < 6 and y_down > -1 and self.board[x_up][y_down] == chip:
                count += 1
                x_up += 1
                y_down -= 1

                return count >= 4

        if across() or up() or diagonal_1() or diagonal_2():
            return True
        else:
            return False