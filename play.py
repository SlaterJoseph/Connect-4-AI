from Game.board import Board
from Game.player import Player
from Visualization.visualizer import BoardVisualizer
import matplotlib.pyplot as plt

print('Starting...')
print('Some info needed. Be aware player 1 goes first.')
option_1 = int(input('What model is player 1? \n1. Human \n2. Minimax\n'))
option_2 = int(input('What model is player 2? \n1. Human \n2. Minimax\n'))

player_1 = Player(option_1)
player_2 = Player(option_2)

game = Board(player_1, player_2)
visualizer = BoardVisualizer(game.get_game())
plt.ion()
plt.show()

player_1.update_board(game.get_game())
player_2.update_board(game.get_game())

terminate = False
player_1_turn = True

while not terminate:
    if player_1_turn:
        print('Player 1\'s move')
        col = player_1.turn()
        ongoing = game.drop(col, player_1)
    else:
        print('Player 2\'s move')
        col = player_2.turn()
        ongoing = game.drop(col, player_2)

    player_1.update_board(game.get_game())
    player_2.update_board(game.get_game())