import math
import time
import traceback
import random

from une_ai.assignments import ConnectFourGame

from connect_four_environment import ConnectFourEnvironment
from une_ai.models import GraphNode, MCTSGraphNode
import algos


# A simple agent program choosing actions randomly
def random_behaviour(percepts, actuators):
    try:
        game_state = {
            'game-board': percepts['game-board-sensor'],
            'power-up-Y': percepts['powerups-sensor']['Y'],
            'power-up-R': percepts['powerups-sensor']['R'],
            'player-turn': percepts['turn-taking-indicator']
        }
    except KeyError as e:
        game_state = {}
        print("You may have forgotten to add the necessary sensors:")
        traceback.print_exc()

    if not ConnectFourEnvironment.is_terminal(game_state):
        legal_moves = ConnectFourEnvironment.get_legal_actions(game_state)
        try:
            action = random.choice(legal_moves)
        except IndexError as e:
            print(
                "You may have forgotten to implement the ConnectFourEnvironment methods, or you implemented them "
                "incorrectly:")
            traceback.print_exc()
            return []

        return [action]
    else:
        return []


# An agent program to allow a human player to play Connect Four
# see the assignment's requirements for a list of valid keys
# to interact with the game
def human_agent(percepts, actuators):
    global action
    game_board = percepts['game-board-sensor']
    power_up_Y = percepts['powerups-sensor']['Y']
    power_up_R = percepts['powerups-sensor']['R']
    player_turn = percepts['turn-taking-indicator']
    game_state = {
        'game-board': game_board.copy(),
        'power-up-Y': power_up_Y,
        'power-up-R': power_up_R,
        'player-turn': player_turn
    }

    if not ConnectFourEnvironment.is_terminal(game_state):
        legal_moves = ConnectFourEnvironment.get_legal_actions(game_state)
        try:
            board = game_state['game-board'].get_map()
            print(board)
            action1 = ConnectFourGame.wait_for_user_input()
            if action1 in legal_moves:
                action = action1

        except IndexError as e:
            print(
                "You may have forgotten to implement the ConnectFourEnvironment methods, or you implemented them "
                "incorrectly:")
            traceback.print_exc()
            return []
        return [action]
    else:
        return []

# TODO
# complete the agent program to implement an intelligent behaviour for
# the agent player
def intelligent_behaviour(percepts, actuator):
    game_board = percepts['game-board-sensor']
    power_up_Y = percepts['powerups-sensor']['Y']
    power_up_R = percepts['powerups-sensor']['R']
    player_turn = percepts['turn-taking-indicator']
    game_state = {
        'game-board': game_board.copy(),
        'power-up-Y': power_up_Y,
        'power-up-R': power_up_R,
        'player-turn': player_turn
    }

    if not ConnectFourEnvironment.is_terminal(game_state):

        # print(game_state['game-board'].get_map()
        board = game_state['game-board'].get_map()
        # col_count = ConnectFourEnvironment.N_COLS
        # row_count = ConnectFourEnvironment.N_ROWS
        # player = game_state['player-turn']

        #print(board)
        # if player == 'Y':
        #     print('Player turn: Y')
        #     col = random.randint(0, col_count)
        #     # print(col)
        #     # action = 'release-{0}'.format(col)
        #     action = random.choice(legal_moves)
        #     # print(action)
        # else:
        #     state_node = GraphNode(board, None, None, 0)
        #     print('Player turn: R')
        #     _, best_move = minimax_algo.minimax(state_node, player, 5)
        #     if best_move is not None:
        #         # return [best_move]
        #         action = [best_move]

        tic = time.time()
        root_node = MCTSGraphNode(game_state, None, None)
        best_move = algos.mcts(root_node, player_turn)
        toc = time.time()
        print("[MTCS (player {0})] Elapsed (sec): {1:.6f}".format(player_turn, toc-tic))
        if best_move is not None:
            return [best_move]
    return []
