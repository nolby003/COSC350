from une_ai.assignments import ConnectFourBaseEnvironment


class ConnectFourEnvironment(ConnectFourBaseEnvironment):

    def __init__(self):
        super().__init__()

    # TODO
    # static method
    # Note: in a static method you do not have access to self
    def get_legal_actions(game_state):
        # it must return the legal actions for the current game state

        # print(game_state)
        game_board = game_state['game-board']  # GridMap object
        power_up_Y = game_state['power-up-Y']  # anvil
        power_up_R = game_state['power-up-R']  # wall
        player_turn = str(game_state['player-turn'])  # Y

        board = game_state['game-board'].get_map()

        if player_turn == 'Y':
            powerup = power_up_Y
        elif player_turn == 'R':
            powerup = power_up_R

        legal_actions = []

        empty_cells = game_board.find_value(None)
        winner = ConnectFourEnvironment.get_winner(game_state)
        if winner is None:
            for empty_cell in empty_cells:

                # Legal release moves
                # release checkers at empty spaces - works
                legal_actions.append('release-{0}'.format(empty_cell[0]))

                # Legal popup moves
                # can only popup own checkers at non-empty spaces - works
                board = game_board.get_map()
                boardrow = list(board[5])
                # print(board[5])
                if player_turn in boardrow:
                    # print('Player: {0}'.format(player))
                    # print('Empty cell: {0}'.format(empty_cell[0]))
                    ind = boardrow.index(player_turn)
                    # print(ind)
                    # print('Index of bottom row: {0}'.format(ind))
                    legal_actions.append('popup-{0}'.format(ind))

                # Legal powerup moves
                # use power up if available - works
                # so long as powerup is not None (Red and Yellow)
                if powerup is not None:
                    legal_actions.append('use-power-up-{0}'.format(empty_cell[0]))

        # print(legal_actions)
        return legal_actions

    # TODO
    # static method
    # Note: in a static method you do not have access to self
    def is_terminal(game_state):
        # # it must return True if there is a winner or there are no more legal actions, False otherwise
        remaining_actions = ConnectFourEnvironment.get_legal_actions(game_state)
        if len(remaining_actions) == 0:
            return True

        winner = ConnectFourEnvironment.get_winner(game_state)
        if winner is not None:
            return True

        return False

    # TODO
    # static method
    # Note: in a static method you do not have access to self
    def payoff(game_state, player_colour):
        # it must return a payoff for the considered player ('Y' or 'R') in a given game_state
        winner = ConnectFourEnvironment.get_winner(game_state)
        print(winner)
        if winner is None:
            return 0
        elif winner == player_colour:
            return 1
        else:
            return -1
