import deck as Deck


# Todo
def miner_behaviour(game_state, options):
    """
    look at hand to see what cards the player has
    look at board to see what valid path cards can be used
    determine whether a path card or action card should be used
    a path card is used when an action card does not need to be and only when a path card is valid to be placed
    based on the current board condition

    an action card may be suitable when a player has been sabotaged with a broken card
    which determines who is a fellow miner
    """

    # board state
    board = game_state['game-board']
    get_board = board.get_map()
    # print(get_board)
    path_list = game_state['path-list']

    # get last path card placed
    lenpl = len(path_list)
    last_card_coord = path_list[lenpl - 1]
    # print(last_card_coord)  # (0, 2)
    last_card = board.get_item_value(last_card_coord[0], last_card_coord[1])
    # print(last_card)  # start

    # player turn (current player)
    player = game_state['player-turn']

    # player hand
    hand = options
    mend_cards = []
    path_cards = []
    # print('hand? {0}'.format(hand))

    # get all path cards
    for card in hand['Path']:
        path_cards.append(card)

    # -------
    # turn to action cards if we do no do a path card
    # -------

    # get all actions cards
    for card in hand['Action']:
        if card.startswith('mend-'):
            mend_cards.append(card)

    # check if there are any sabotage cards given to players
    actions_list = game_state['actions-given']
    if len(actions_list) > 0:
        for key in actions_list:
            if key is not player:
                for val in actions_list[key]:
                    card = actions_list[key][val]
                    if card.startswith('sab-'):
                        sab_cards = {key: card}

    # -------


def saboteur_behaviour(game_state, options):
    pass
