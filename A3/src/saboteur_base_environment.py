import random
import numpy as np
from scipy.signal import convolve2d, convolve

from une_ai.models import GameEnvironment
from une_ai.models import GridMap


class InvalidMoveException(Exception):
    pass


class SaboteurBaseEnvironment(GameEnvironment):
    N_COLS = 20
    N_ROWS = 20

    def __init__(self):
        super().__init__("Saboteur Game Environment")
        self._game_board = GridMap(SaboteurBaseEnvironment.N_COLS, SaboteurBaseEnvironment.N_ROWS, None)
        # self._played_powerup = (None, None)
        self._player_turn = 'Gold-Digger'

    def add_player(self, player):
        pass

    def get_game_state(self):
        game_state = {
            'game-board': self._game_board.copy(),
            'player-turn': self._player_turn
        }

        return game_state

    def turn(game_state):
        pass

    def get_winner(game_state):
        pass

    def get_percepts(self):
        pass

    def _change_player_turn(self):
        pass

    def transition_result(game_state, action):
        pass

    def state_transition(self, agent_actuators):
        pass