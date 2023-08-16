from connect_four_environment import ConnectFourEnvironment as gm
from une_ai.models import GraphNode

import random
import time
import math


def minimax(node, player, depth):
    move_best = None

    game_state = node.get_state()
    player_turn = game_state['player-turn']
    is_maximising = player_turn == player

    if is_maximising:
        value = float('-Inf')
    else:
        value = float('+Inf')
    if depth <= 0 or gm.is_terminal(game_state):
        value = gm.payoff(game_state, player)
        return value, move_best

    legal_actions = gm.get_legal_actions(game_state)
    for action in legal_actions:
        new_state = gm.transition_result(game_state, action)
        child_node = GraphNode(new_state, node, action, 1)
        value_new, _ = minimax(child_node, player, depth - 1)
        if (is_maximising and value_new > value) or (not is_maximising and value_new < value):
            value = value_new
            move_best = action

    return value, move_best


def minimax_alpha_beta(node, player, alpha, beta, depth):
    game_state = node.get_state()
    move_best = None
    legal_actions = gm.get_legal_actions(game_state)

    player_turn = game_state['player-turn']
    is_maximising = player_turn == player

    if is_maximising:
        value = float('-Inf')
    else:
        value = float('+Inf')
    if depth <= 0 or gm.is_terminal(game_state):
        value = gm.payoff(game_state, player)
        return value, move_best

    for action in legal_actions:
        new_state = gm.transition_result(game_state, action)
        child_node = GraphNode(new_state, node, action, 1)
        value_new, _ = minimax_alpha_beta(child_node, player, alpha, beta, depth - 1)
        if is_maximising:
            if value_new > value:
                value = value_new
                move_best = action
            alpha = max(value, alpha)
            if value >= beta:
                break
        else:
            if value_new < value:
                value = value_new
                move_best = action
            beta = min(value, beta)
            if value <= alpha:
                break

    return value, move_best


def optimised_minimax(node, player, tt, depth):
    game_state = node.get_state()
    player_turn = game_state['player-turn']
    is_maximising = player_turn == player

    # using transposition table
    tt_entry = tt.lookup(node)
    if tt_entry is not None and tt_entry['depth'] >= depth:
        return tt_entry['value'], tt_entry["move_best"]

    move_best = None

    if is_maximising:
        value = float('-Inf')
    else:
        value = float('+Inf')
    if depth <= 0 or gm.is_terminal(game_state):
        value = gm.payoff(game_state, player)
        return value, move_best

    legal_actions = gm.get_legal_actions(game_state)
    for action in legal_actions:
        new_state = gm.transition_result(game_state, action)
        child_node = GraphNode(new_state, node, action, 1)
        value_new, _ = optimised_minimax(child_node, player, tt, depth - 1)

        if (is_maximising and value_new > value) or (not is_maximising and value_new < value):
            value = value_new
            move_best = action

    # storing value in transposition table
    if tt_entry is None or tt_entry['depth'] <= depth:
        entry_dict = {
            "value": int(value),
            "depth": depth,
            "move_best": move_best
        }

        tt.store_node(node, entry_dict)

    return value, move_best


def selection_policy(node, target_player):
    # In this case, we select a node that was not explored yet
    # or, if all nodes were explored, the one with highest wins
    # Better version may use different policies (e.g. see UCT policy)
    successors = node.get_successors()
    best_uct_score = 0
    best_node = None
    for s in successors:
        if s.n() > 0:
            uct = (s.wins(target_player) / s.n()) + math.sqrt(2) * math.sqrt(math.log(s.get_parent_node().n()) / s.n())
            if best_node is None or uct > best_uct_score:
                best_uct_score = uct
                best_node = s
        else:
            # unexplored child, choose it
            return s

    return best_node


def random_playout(initial_node):
    current_playout_state = initial_node.get_state()
    while not gm.is_terminal(current_playout_state):
        possible_moves = gm.get_legal_actions(current_playout_state)
        action = random.choice(possible_moves)
        current_playout_state = gm.transition_result(current_playout_state, action)

    return gm.get_winner(current_playout_state)


def mcts(root_node, target_player, max_time=1):
    start_time = time.time()

    # Performing simulations until the time is up
    while (time.time() - start_time) < max_time:
        # SELECTION PHASE
        current_node = root_node
        while not gm.is_terminal(current_node.get_state()) and not current_node.is_leaf_node():
            current_node = selection_policy(current_node, target_player)

        # EXPANSION PHASE
        selected_node = current_node
        legal_moves = gm.get_legal_actions(selected_node.get_state())
        for a in legal_moves:
            if not selected_node.was_action_expanded(a):
                successor_state = gm.transition_result(selected_node.get_state(), a)
                selected_node.add_successor(successor_state, a)

        # SIMULATION PHASE
        winner = random_playout(selected_node)
        if winner is None:
            # we consider a tie as a win
            # if we don't do that, we might find an optimal opponent
            # always 1 step ahead of us and the only best option
            # for us is to achieve a tie
            winner = target_player

        # BACKPROPAGATION PHASE
        selected_node.backpropagate(winner)

    # Time is up, choosing the child of the root node with highest wins
    best_node = None
    max_wins = 0
    for successor in root_node.get_successors():
        if best_node is None or successor.wins(target_player) / successor.n() > max_wins:
            best_node = successor
            max_wins = successor.wins(target_player) / successor.n()
    return best_node.get_action()
