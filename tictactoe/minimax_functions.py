from tictactoe_game_environment import TicTacToeGameEnvironment as gm
from une_ai.models import GraphNode

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