def agent_program_minimax(percepts, actuators, max_depth=4):
    game_board = percepts['game-board-sensor']
    player_turn = percepts['turn-taking-indicator']
    game_state = {
        'game-board': game_board.copy(),
        'player-turn': player_turn
    }

def miner_behaviour(percepts, actuators):
    pass

def saboteur_behaviour(percepts, actuators):
    pass