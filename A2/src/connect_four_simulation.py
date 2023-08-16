import logging

from connect_four_environment import ConnectFourEnvironment
from connect_four_player import ConnectFourPlayer

class ConnectFourSimulation():

    def __init__(self, yellow_player, red_player, verbose=False):
        assert isinstance(yellow_player, ConnectFourPlayer), "The parameter yellow_player must be an instance of the class ConnectFourPlayer"
        assert isinstance(red_player, ConnectFourPlayer), "The parameter yellow_player must be an instance of the class ConnectFourPlayer"

        self._env = None
        self._verbose = verbose
        self._logger = None
        if self._verbose:
            logging.basicConfig()
            logging.root.setLevel(logging.NOTSET)
            self._logger = logging.getLogger("ConnectFourSimulation")

        self._players = {
            'Y': yellow_player,
            'R': red_player
        }
    
    def log(self, message):
        if self._verbose:
            self._logger.info(message)
    
    def run_simulation(self):
        self._env = ConnectFourEnvironment()
        self._env.add_player(self._players['Y'])
        self._env.add_player(self._players['R'])
        winner = False
        plys = []
        while (winner == False):
            winner, cur_ply = self._play()
            plys.append(cur_ply)
        
        return winner, plys

    def _play(self):
        cur_ply = {}
        game_state = self._env.get_game_state()
        game_board = game_state['game-board'].get_map()
        self.log("Current game board")
        self.log(game_board)
        cur_ply['game-state'] = {
            'game-board': game_board.tolist(),
            'player-turn': game_state['player-turn'],
            'power-up-Y': game_state['power-up-Y'],
            'power-up-R': game_state['power-up-R']
        }
        if ConnectFourEnvironment.is_terminal(game_state):
            self.log("Reached a terminal state")
            return ConnectFourEnvironment.get_winner(game_state), cur_ply
        
        cur_colour = ConnectFourEnvironment.turn(game_state)
        
        # SENSE
        self._players[cur_colour].sense(self._env)
        # THINK
        actions = self._players[cur_colour].think()
        cur_ply['action'] = actions
        player = 'Yellow' if cur_colour == 'Y' else 'Red'
        if len(actions) != 0:
            cur_action = "{0} player played the move '{1}'".format(player, actions[0])
            self.log(cur_action)
        # ACT
        self._players[cur_colour].act(actions, self._env)

        return False, cur_ply
    
