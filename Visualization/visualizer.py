import matplotlib.pyplot as plt
import numpy as np

class BoardVisualizer:
    def __init__(self, board):
        self.board = board
        self.n_rows = len(board)
        self.n_cols = len(board[0])

        self.fig, self.ax = plt.subplots()
        self.ax.set_xticks(np.arange(self.n_cols))
        self.ax.set_yticks(np.arange(self.n_rows))
        self.ax.grid(True, which='both', color='black', linestyle='-', linewidth=2)

        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        plt.axis('off')  # Hide axes for a cleaner look

        self.text_objects = [[self.ax.text(j, i, '', va='center', ha='center', fontsize=18)
                              for j in range(self.n_cols)] for i in range(self.n_rows)]

    def update_board(self, new_board):
        """
        Update the board visualization with new values.
        new_board: The updated 2D board list
        """
        self.board = new_board

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                self.text_objects[i][j].set_text(str(self.board[i][j]))

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()