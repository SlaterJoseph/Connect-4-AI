from Game.board import Board


def minimax(player, game: Board, time_remaining, depth: int) -> tuple:
    """
    The base call of the minimax search
    :param player: The player making the move (our agent)
    :param game: The current game state
    :param time_remaining: The amount of time before a move MUST be returned
    :param depth: The max depth the search will reach
    :return: A move, value tuple
    """
    val, action = get_max(player, game, depth, time_remaining, False)
    return action


def get_max(player, game: Board, depth: int, time_left, terminate: bool) -> tuple:
    """
    A function which finds the highest evaluated move of the children
    :param player: The player making the move (our agent)
    :param game: The current game state
    :param depth: The remaining depth to search
    :param time_left: The time left we have to search before a force return
    :param terminate: A boolean to know if we should terminate early
    :return: A value, move tuple
    """
    if terminate:
        return player.utility(game), None

    if depth == 0:
        return player.utility(game), None

    if time_left() <= 100:
        return player.utility(game), None

    val = float('-inf')
    actions = game.get_actions()
    move = actions[0]

    for action in actions:
        new_state, result = game.forecast_move(action)

        if result == 1:
            new_val = float('inf')
        elif result == 2:
            new_val = 0
        else:
            new_val, _ = get_min(new_state, game, depth - 1, time_left, False)

        if new_val > val:
            val = new_val
            move = action

    return val, move


def get_min(player, game: Board, depth: int, time_left, terminate: bool) -> tuple:
    """
    A function which finds the lowest evaluated move of the children
    :param player: The current player making the move (our agent)
    :param game: The game state
    :param depth: The remaining depth to search
    :param time_left: The time left before a force return
    :param terminate: A boolean to know if we should terminate early
    :return: A value, move tuple
    """
    if terminate:
        return player.utility(game), None

    if depth == 0:
        return player.utility(game), None

    val = float('inf')
    actions = game.get_actions()
    move = actions[0]

    for action in actions:
        new_state, result = game.forecast_move(action)

        if result == 1:
            new_val = float('-inf')
        elif result == 2:
            new_val = 0
        else:
            new_val, _ = get_max(new_state, game, depth - 1, time_left, False)

        if new_val < val:
            val = new_val
            move = action

    return val, move

