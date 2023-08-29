from saboteur_game import SaboteurGame
from saboteur_environment import SaboteurEnvironment
from saboteur_player import SaboteurPlayer

PYGAME_DETECT_AVX2 = 1

if __name__ == '__main__':
    game_environment = SaboteurEnvironment()
    game = SaboteurGame(game_environment)
