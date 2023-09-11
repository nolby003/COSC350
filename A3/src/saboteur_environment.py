from saboteur_base_environment import SaboteurBaseEnvironment


class SaboteurEnvironment(SaboteurBaseEnvironment):

    # initialize
    def __init__(self):
        super().__init__()

    # legal actions/moves
    def get_legal_actions(game_state):
        game_board = game_state['game-board']  # GridMap object
        playerss = game_state['players']
        player_turn = str(game_state['player-turn'])
        player_hand = str(game_state['player-hand'])
        board = game_state['game-board'].get_map()
        remaining_cards = str(game_state['remaining-cards'])

        legal_actions = []
        player_cards = []
        for val in player_hand[1]:
            player_cards.append(val)
        legal_actions = player_cards
        legal_actions.extend(remaining_cards)
        # print(legal_actions)
        return legal_actions

    # When gamestate ends
    def is_terminal(game_state):
        remaining_actions = SaboteurEnvironment.get_legal_actions(game_state)
        if len(remaining_actions) == 0:
            return True

        winner = SaboteurEnvironment.get_winner(game_state)
        if winner is not None:
            return True

        return False

    # winner payoff
    def payoff(game_state, player):
        # it must return a payoff for the considered player ('Y' or 'R') in a given game_state
        winner = SaboteurEnvironment.get_winner(game_state)
        print(winner)
        if winner is None:
            return 0
        elif winner == player:
            return 1
        else:
            return -1
