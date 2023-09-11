import numpy as np
from une_ai.models import GameEnvironment, GridMap


class IllegalMove(Exception):
    pass


class SaboteurGameEnvironment(GameEnvironment):
    VALID_BOX = lambda v: v is None or (
            isinstance(v, tuple) and len(v) == 2 and v[0] in range(0, 3) and v[1] in range(0, 3))

    def __init__(self, player_X, player_O):
        super().__init__("Saboteur")

        self._game_board = GridMap(20, 20, None)
        agent_name = self.add_player(player_X)
        self._agent_X = agent_name
        agent_name = self.add_player(player_O)
        self._agent_O = agent_name

    def get_game_state(self):
        return self._game_board.copy()

    def get_legal_actions(game_state):
        legal_actions = []
        empty_boxes = game_state.find_value(None)
        for empty_box in empty_boxes:
            legal_actions.append('mark-{0}-{1}'.format(empty_box[0], empty_box[1]))

        return legal_actions

    def is_terminal(game_state):
        # game is over if the board is full
        remaining_actions = SaboteurGameEnvironment.get_legal_actions(game_state)
        if len(remaining_actions) == 0:
            return True

        # or if there is a winner
        winner = SaboteurGameEnvironment.get_winner(game_state)
        if winner is not None:
            return True

        return False

    def get_player_name(self, marker):
        if marker == 'X':
            return self._agent_X
        else:
            return self._agent_O

    def get_winner(game_state):
        h = game_state.get_height()
        w = game_state.get_width()

        # check rows
        for i in range(0, h):
            cur_row = game_state.get_row(i)
            first_symbol = cur_row[0]
            if first_symbol is None:
                # no winning row for sure
                continue
            if cur_row[0] == cur_row[1] == cur_row[2]:
                # winner
                return first_symbol

        # check cols
        for i in range(0, w):
            cur_col = game_state.get_column(i)
            first_symbol = cur_col[0]
            if first_symbol is None:
                # no winning row for sure
                continue
            if cur_col[0] == cur_col[1] == cur_col[2]:
                # winner
                return first_symbol

        # check diagonals
        board = game_state.get_map()
        if board[1, 1] is not None and (
                (board[0, 0] == board[1, 1] == board[2, 2]) or (board[2, 0] == board[1, 1] == board[0, 2])):
            return board[1, 1]

        return None

    def turn(game_state):
        n_x = len(game_state.find_value('X'))
        n_o = len(game_state.find_value('O'))

        if n_x == n_o:
            # X always start, so X turn
            return 'X'
        else:
            return 'O'

    def transition_result(game_state, action):
        legal_actions = SaboteurGameEnvironment.get_legal_actions(game_state)
        if action not in legal_actions:
            raise (IllegalMove('The action {0} is not a legal move for the given game state {1}.'.format(action,
                                                                                                         game_state.get_map())))

        marker = SaboteurGameEnvironment.turn(game_state)

        tokens = action.split('-')
        x, y = (int(tokens[1]), int(tokens[2]))
        new_game_state = game_state.copy()
        new_game_state.set_item_value(x, y, marker)

        return new_game_state

    def payoff(game_state, player_name):
        winner = SaboteurGameEnvironment.get_winner(game_state)
        if winner is None:
            return 0
        elif winner == player_name:
            return 1
        else:
            return -1

    def get_percepts(self):
        return {'game-board-sensor': self.get_game_state()}

    def state_transition(self, agent_actuators):
        cur_state = self.get_game_state()
        marker_turn = SaboteurGameEnvironment.turn(cur_state)
        player_turn = self.get_player_name(marker_turn)
        box_coord = agent_actuators['marker']
        if box_coord is not None:
            self.mark_box(box_coord[0], box_coord[1], player_turn)

    def mark_box(self, x, y, player_name):
        if player_name == self._agent_X:
            mark = 'X'
        else:
            mark = 'O'

        if self._game_board.get_item_value(x, y) is None:
            self._game_board.set_item_value(x, y, mark)
        else:
            raise (IllegalMove("Illegal move. Box at ({0}, {1}) already marked with {2}.".format(x, y,
                                                                                                 self._game_board.get_item_value(
                                                                                                     x, y))))
