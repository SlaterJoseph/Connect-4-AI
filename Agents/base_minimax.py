def minimax(player, game, time_remaining, depth) -> tuple:
    """
    The base call of the minimax search
    :param player: The player making the move (our agent)
    :param game: The current game state
    :param time_remaining: The amount of time before a move MUST be returned
    :param depth: The max depth the search will reach
    :return: A move, value tuple
    """
    pass


def get_max(player, game, depth, time_left, terminate):
    if terminate:
        return player.utility(game), None

    if depth == 0:
        return player.utility(game), None

    val = float('-inf')
