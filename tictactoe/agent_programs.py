import random
import time

from une_ai.models import GraphNode, MCTSGraphNode

from tictactoe_game_environment import TicTacToeGameEnvironment
from minimax_functions import minimax, minimax_alpha_beta, optimised_minimax
from MCTS_functions import mcts

def agent_program_random(percepts, actuators):
    try:
        game_board = percepts['game-board-sensor']
        player_turn = percepts['turn-taking-indicator']
        game_state = {
            'game-board': game_board.copy(),
            'player-turn': player_turn
        }
    except KeyError:
        print("Error. You may have not fully implemented yet the class TicTacToeGameEnvironment")
        return []
    
    legal_moves = TicTacToeGameEnvironment.get_legal_actions(game_state)
    if len(legal_moves) > 0:
        return [random.choice(legal_moves)]
    
    return []

def agent_program_minimax(percepts, actuators, max_depth=4):
    game_board = percepts['game-board-sensor']
    player_turn = percepts['turn-taking-indicator']
    game_state = {
        'game-board': game_board.copy(),
        'player-turn': player_turn
    }

    
    if not TicTacToeGameEnvironment.is_terminal(game_state):
        state_node = GraphNode(game_state, None, None, 0)
        print(game_state)
        tic = time.time()
        _, best_move = minimax(state_node, player_turn, max_depth)
        toc = time.time()
        print("[Minimax (player {0})] Elapsed (sec): {1:.6f}".format(player_turn, toc-tic))
        if best_move is not None:
            return [best_move]
    
    return []

def agent_program_minimax_alpha_beta(percepts, actuators, max_depth=4):
    game_board = percepts['game-board-sensor']
    player_turn = percepts['turn-taking-indicator']
    game_state = {
        'game-board': game_board.copy(),
        'player-turn': player_turn
    }
    
    if not TicTacToeGameEnvironment.is_terminal(game_state):
        state_node = GraphNode(game_state, None, None, 0)
        tic = time.time()
        _, best_move = minimax_alpha_beta(state_node, player_turn, float("-Inf"), float("+Inf"), max_depth)
        toc = time.time()
        print("[Minimax Alpha-Beta (player {0})] Elapsed (sec): {1:.6f}".format(player_turn, toc-tic))
        if best_move is not None:
            return [best_move]
    
    return []

def agent_program_mcts(percepts, actuators, max_time=1):
    game_board = percepts['game-board-sensor']
    player_turn = percepts['turn-taking-indicator']
    game_state = {
        'game-board': game_board.copy(),
        'player-turn': player_turn
    }

    if not TicTacToeGameEnvironment.is_terminal(game_state):
        tic = time.time()
        root_node = MCTSGraphNode(game_state, None, None)
        best_move = mcts(root_node, player_turn, max_time)
        toc = time.time()
        print("[MTCS (player {0})] Elapsed (sec): {1:.6f}".format(player_turn, toc-tic))
        if best_move is not None:
            return [best_move]
    
    return []

def agent_program_optimised_minimax(percepts, actuators, tt, max_depth=4):
    game_board = percepts['game-board-sensor']
    player_turn = percepts['turn-taking-indicator']
    game_state = {
        'game-board': game_board.copy(),
        'player-turn': player_turn
    }

    
    if not TicTacToeGameEnvironment.is_terminal(game_state):
        state_node = GraphNode(game_state, None, None, 0)
        tic = time.time()
        _, best_move = optimised_minimax(state_node, player_turn, tt, max_depth)
        toc = time.time()
        print("[Optimised Minimax (player {0})] Elapsed (sec): {1:.6f}".format(player_turn, toc-tic))
        if best_move is not None:
            return [best_move]
    
    return []

