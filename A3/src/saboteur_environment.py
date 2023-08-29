from saboteur_base_environment import SaboteurBaseEnvironment


class SaboteurEnvironment(SaboteurBaseEnvironment):

    # initialize
    def __init__(self):
        super().__init__()

    # legal actions/moves
    def get_legal_actions(game_state):
        pass

    # When gamestate ends
    def is_terminal(game_state):
        pass

    # winner payoff
    def payoff(game_state, player):
        pass
