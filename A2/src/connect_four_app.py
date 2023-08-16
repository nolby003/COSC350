from une_ai.assignments import ConnectFourGame
from connect_four_environment import ConnectFourEnvironment
from connect_four_player import ConnectFourPlayer
from agent_programs import random_behaviour, human_agent, intelligent_behaviour

PYGAME_DETECT_AVX2 = 1

if __name__ == '__main__':
    # Change these two lines to instantiate players with proper
    # agent programs, as per your tests

    # ------------------------------------
    # choose test scenario below
    agent_choice = 6
    # 1: random vs random
    # 2: intelligent vs intelligent
    # 3: human vs human
    # 4: random vs intelligent
    # 5: human vs random
    # 6: human vs intelligent

    # random vs random
    if agent_choice == 1:
        player1 = random_behaviour
        player2 = random_behaviour

    # intelligent vs intelligent
    elif agent_choice == 2:
        player1 = intelligent_behaviour
        player2 = intelligent_behaviour

    # human vs human
    elif agent_choice == 3:
        player1 = human_agent
        player2 = human_agent

    # random vs intelligent
    elif agent_choice == 4:
        player1 = random_behaviour
        player2 = intelligent_behaviour

    # human vs random
    elif agent_choice == 5:
        player1 = human_agent
        player2 = random_behaviour

    # human vs intelligent
    elif agent_choice == 6:
        player1 = human_agent
        player2 = intelligent_behaviour
    # ------------------------------------

    yellow_player = ConnectFourPlayer('Y', player1)
    red_player = ConnectFourPlayer('R', player2)

    # DO NOT EDIT THESE LINES OF CODE!!!
    game_environment = ConnectFourEnvironment()
    game_environment.add_player(yellow_player)
    game_environment.add_player(red_player)

    game = ConnectFourGame(yellow_player, red_player, game_environment)
