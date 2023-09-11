from saboteur_game import SaboteurGame
from saboteur_environment import SaboteurEnvironment
from saboteur_player import SaboteurPlayer
from agent_programs import miner_behaviour, saboteur_behaviour

PYGAME_DETECT_AVX2 = 1

if __name__ == '__main__':
    agent_miner = SaboteurPlayer('Miner', miner_behaviour)
    agent_saboteur = SaboteurPlayer('Saboteur', saboteur_behaviour)
    environment = SaboteurEnvironment()
    environment.add_player(agent_miner)
    environment.add_player(agent_saboteur)
    nplayers = 3
    SaboteurGame(agent_miner, agent_saboteur, environment, nplayers)  # how many players to pass in?
