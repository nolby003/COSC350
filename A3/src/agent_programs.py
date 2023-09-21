from deck import Deck


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

    # Todo - What does the current game board state look like?
    board = game_state['game-board']
    get_board = board.get_map()
    # print(get_board)

    # Todo - What was the last path card placed?
    path_list = game_state['path-list']
    # get last path card placed
    lenpl = len(path_list)
    last_card_coord = path_list[lenpl - 1]
    # print(last_card_coord)  # (0, 2)
    last_card = board.get_item_value(last_card_coord[0], last_card_coord[1])
    # print(last_card)  # start

    # Todo - Who am I as the current player?
    # player turn (current player)
    player = game_state['player-turn']

    # Todo - What is my current hand?
    # player hand
    hand = options
    mend_cards = []
    path_cards = []
    # print('hand? {0}'.format(hand))

    result = False

    # Todo - What path cards do I have?
    # get all path cards
    for card in hand['Path']:
        path_cards.append(card)

    # Todo - What action cards do I have relative to my group?
    # get all actions cards
    for card in hand['Action']:
        if card.startswith('mend_'):
            card0 = str(card).partition('_')
            mend_cards.append(card0)

    # Todo - What play should I make? Place a path card or play an action card?

    # Todo - Let's check if any players currently have any sabotage cards, if not, then we can look at path cards
    # check if there are any sabotage cards given to players
    sab_cards = {}
    actions_list = game_state['actions-given']
    if len(actions_list) > 0:
        for key in actions_list:
            if key is not player:  # need to ensure it is not me with a card
                for val in actions_list[key]:
                    card = actions_list[key][val]
                    if card.startswith('sab_'):
                        sab_cards = {key: card}
    # Todo - If yes, let's get the information of the player and the card
    ctype = ''
    # print(len(sab_cards))
    if len(sab_cards) > 0:
        ctype = ''
        for key in sab_cards:
            card = sab_cards[key]
            p = key
            print('Player {0} has a sabotage card {1}'.format(key, card))
            ctype = str(card).partition('_')
            print(ctype[1])

        # Todo - iterate over mend cards I have
        p = ''
        for card in mend_cards:
            if card == ctype[1]:  # Todo - if I have a mend card that matches another player's sabotage card, play card
                result = (card, 'Action', 0, 0, p)
            else:
                result = False

    # Todo - if we are not playing an action card, let's work on playing a path card
    if result is False:

        # Todo - I need to validate what path cards I have that are valid to place on the board
        # path card validations
        # go through path cards in hand and look for a card that is a valid conduit to last card played
        last_card_validate = Deck.validation[last_card]  # e.g. start
        # print(last_card_validate)
        validate_dict = {}
        for card in path_cards:
            key = card
            value = Deck.validation[key]
            validate_dict[key] = value

        # print(validate_dict)

        # declare variables
        play_card = ''
        x = 0
        y = 0
        p = ''
        key_list = list(validate_dict.keys())
        print(key_list)
        val_list = list(validate_dict.values())
        print(val_list)
        for card in validate_dict:
            # find the card that can conduit to the last card played and choose that card

            # check East connection
            if validate_dict[card][3] == 1 and last_card_validate[1] == 1:
                play_card_pos = val_list.index(validate_dict[card])
                play_card = key_list[play_card_pos]
                card_coords = (last_card_coord[0]+1, last_card_coord[1])
                x = card_coords[0]
                y = card_coords[1]

            # check North connection
            elif validate_dict[card][2] == 1 and last_card_validate[0] == 1:
                play_card_pos = val_list.index(validate_dict[card])
                play_card = key_list[play_card_pos]
                card_coords = (last_card_coord[0], last_card_coord[1]-1)
                x = card_coords[0]
                y = card_coords[1]

            # check South connection
            elif validate_dict[card][0] == 1 and last_card_validate[2] == 1:
                play_card_pos = val_list.index(validate_dict[card])
                play_card = key_list[play_card_pos]
                card_coords = (last_card_coord[0], last_card_coord[1] + 1)
                x = card_coords[0]
                y = card_coords[1]

        result = (play_card, 'Path', x, y, p)

    return result


def saboteur_behaviour(game_state, options):
    """
    look at hand to see what cards the player has
    look at board to see what valid path cards can be used
    determine whether a path card or action card should be used
    a path card is used when an action card does not need to be and only when a path card is valid to be placed
    based on the current board condition

    an action card may be suitable when a player has been identified as a miner, a sabotage
    card will be given to block them
    """

    # Todo - What does the current game board state look like?
    board = game_state['game-board']
    get_board = board.get_map()
    # print(get_board)

    # Todo - What was the last path card placed?
    path_list = game_state['path-list']
    # get last path card placed
    lenpl = len(path_list)
    last_card_coord = path_list[lenpl - 1]
    # print(last_card_coord)  # (0, 2)
    last_card = board.get_item_value(last_card_coord[0], last_card_coord[1])
    # print(last_card)  # start

    # Todo - Who am I as the current player?
    # player turn (current player)
    player = game_state['player-turn']

    # Todo - What is my current hand?
    # player hand
    hand = options
    mend_cards = []
    path_cards = []
    # print('hand? {0}'.format(hand))

    result = False

    # Todo - What path cards do I have?
    # get all path cards
    for card in hand['Path']:
        path_cards.append(card)

    # Todo - What action cards do I have relative to my group?
    # get all actions cards
    for card in hand['Action']:
        if card.startswith('mend_'):
            card0 = str(card).partition('_')
            mend_cards.append(card0)

    # Todo - What play should I make? Place a path card or play an action card?

    # Todo - Let's check if any players currently have any sabotage cards, if not, then we can look at path cards
    # check if there are any sabotage cards given to players
    sab_cards = {}
    actions_list = game_state['actions-given']
    if len(actions_list) > 0:
        for key in actions_list:
            if key is not player:  # need to ensure it is not me with a card
                for val in actions_list[key]:
                    card = actions_list[key][val]
                    if card.startswith('sab_'):
                        sab_cards = {key: card}
    # Todo - If yes, let's get the information of the player and the card
    ctype = ''
    # print(len(sab_cards))
    if len(sab_cards) > 0:
        ctype = ''
        for key in sab_cards:
            card = sab_cards[key]
            p = key
            print('Player {0} has a sabotage card {1}'.format(key, card))
            ctype = str(card).partition('_')
            print(ctype[1])

        # Todo - iterate over mend cards I have
        p = ''
        for card in mend_cards:
            if card == ctype[1]:  # Todo - if I have a mend card that matches another player's sabotage card, play card
                result = (card, 'Action', 0, 0, p)
            else:
                result = False

    # Todo - if we are not playing an action card, let's work on playing a path card
    if result is False:

        # Todo - I need to validate what path cards I have that are valid to place on the board
        # path card validations
        # go through path cards in hand and look for a card that is a valid conduit to last card played
        last_card_validate = Deck.validation[last_card]  # e.g. start
        # print(last_card_validate)
        validate_dict = {}
        for card in path_cards:
            key = card
            value = Deck.validation[key]
            validate_dict[key] = value

        # print(validate_dict)

        # declare variables
        play_card = ''
        x = 0
        y = 0
        p = ''
        key_list = list(validate_dict.keys())
        print(key_list)
        val_list = list(validate_dict.values())
        print(val_list)
        for card in validate_dict:
            # find the card that can conduit to the last card played and choose that card

            # check East connection
            if validate_dict[card][3] == 1 and last_card_validate[1] == 1:
                play_card_pos = val_list.index(validate_dict[card])
                play_card = key_list[play_card_pos]
                card_coords = (last_card_coord[0] + 1, last_card_coord[1])
                x = card_coords[0]
                y = card_coords[1]

            # check North connection
            elif validate_dict[card][2] == 1 and last_card_validate[0] == 1:
                play_card_pos = val_list.index(validate_dict[card])
                play_card = key_list[play_card_pos]
                card_coords = (last_card_coord[0], last_card_coord[1] - 1)
                x = card_coords[0]
                y = card_coords[1]

            # check South connection
            elif validate_dict[card][0] == 1 and last_card_validate[2] == 1:
                play_card_pos = val_list.index(validate_dict[card])
                play_card = key_list[play_card_pos]
                card_coords = (last_card_coord[0], last_card_coord[1] + 1)
                x = card_coords[0]
                y = card_coords[1]

        result = (play_card, 'Path', x, y, p)

    return result
