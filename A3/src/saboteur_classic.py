import random
import pygame
import numpy as np

from une_ai.models import GridMap
from card import PathCard
from deck import Deck

from une_ai.models import Agent
from agent_programs import miner_behaviour, saboteur_behaviour

BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (125, 125, 125)
BLUE = (10, 20, 200)
GREEN = (255, 125, 125)

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
BOX_SIZE = 80

NCOLS = 9
NROWS = 9


class SaboteurGame():
    play_hand = ['path', 'mend', 'sab', 'discard']

    def __init__(self, agent_miner, agent_saboteur, nplayers, display_w=DISPLAY_WIDTH, display_h=DISPLAY_HEIGHT
                 , box_size=BOX_SIZE):

        self._board = GridMap(NCOLS, NROWS, None)
        self._player_turn = None  # int - player turn init
        self._player_hand = {}  # dict - each player's hand

        self._nplayers = nplayers  # int - number of players
        self._players = {}  # dict - number of players
        self._player_turns = []  # list - player turns in a set order

        self._deck = []  # list - deck of path and action cards
        self._decks = {}  # dict - of all decks in game (path, action, nugget, dwarf)
        self._dwarf_card_deck = []  # list - deck of dwarf cards
        self._action_card_deck = []  # list - deck of action cards
        self._path_card_deck = []  # list - deck of path cards
        self._nugget_card_deck = []  # list - deck of nugget cards
        self._remaining_cards = []  # list - of remaining cards within deck

        self._path_list = []  # list - list of path cards placed on board
        self._discard_deck = []  # list - list of cards in discard pile (from player hands)

        self._action_given = {}  # list - action cards given to players

        self.memory_map = {}  # dict - a map from each player's perspective of each player and their actions
        # the map helps to build inference to what other players are doing
        # helps to understand a determination of whether a player is a miner or saboteur

        # pygame game window init and setup
        pygame.init()
        window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('Saboteur Card Game')
        window_clock = pygame.time.Clock()

        self._box_size = box_size
        self._display = window
        self._window_clock = window_clock
        self._display_size = (display_w, display_h)
        self._n_cols = NCOLS
        self._n_rows = NROWS
        self._padding_left = int((self._display_size[0] - NCOLS * self._box_size) / 2)
        self._padding_top = int((self._display_size[1] - NCOLS * self._box_size) / 2)

        self._agents = {'Miner': agent_miner, 'Saboteur': agent_saboteur}
        self._card_reveal = False

        # build x and y cartesian coords into board
        self._coordinates = np.array([[None] * self._n_cols] * self._n_rows)
        for y in range(self._n_rows):
            for x in range(self._n_cols):
                self._coordinates[y, x] = (x, y)

        # define fonts
        fonts = pygame.font.get_fonts()
        self._font = fonts[0]  # default to a random font
        # try to look among the most common fonts
        test_fonts = ['arial', 'couriernew', 'verdana', 'helvetica', 'roboto']
        for font in test_fonts:
            if font in fonts:
                self._font = font
                break

        # --------------------------------------------------------
        # INITIALIZATION AND SETUP
        #
        # SETTING UP DECKS
        # --------------------------------------------------------

        # --------------------------------------------------------
        # Path cards
        # --------------------------------------------------------
        path_card_deck = []
        for i in range(4):
            path_card_deck.append('NSC')
        for i in range(5):
            path_card_deck.append('NSEC')
        for i in range(5):
            path_card_deck.append('NSEWC')
        for i in range(5):
            path_card_deck.append('NEWC')
        for i in range(3):
            path_card_deck.append('EWC')
        for i in range(4):
            path_card_deck.append('NEC')
        for i in range(5):
            path_card_deck.append('NWC')
        path_card_deck.append('S')
        path_card_deck.append('NS')
        path_card_deck.append('NSE')
        path_card_deck.append('NSEW')
        path_card_deck.append('NEW')
        path_card_deck.append('EW')
        path_card_deck.append('SE')
        path_card_deck.append('SW')
        path_card_deck.append('W')
        self._path_card_deck = path_card_deck
        path_cards = {'PathCard': path_card_deck}
        # --------------------------------------------------------

        # --------------------------------------------------------
        # Action cards
        # --------------------------------------------------------
        action_card_deck = []
        for i in range(6):
            action_card_deck.append('map')
        # for i in range(9):
        action_card_deck.append('sab_axe')
        action_card_deck.append('sab_cart')
        action_card_deck.append('sab_lant')
        # for i in range(9):
        action_card_deck.append('mend_lantcart')
        action_card_deck.append('mend_axelant')
        action_card_deck.append('mend_axecart')
        action_card_deck.append('mend_cart')
        action_card_deck.append('mend_axe')
        action_card_deck.append('mend_lant')

        for i in range(3):
            action_card_deck.append('dynamite')
        action_cards = {'ActionCard': action_card_deck}
        self._action_card_deck = action_card_deck
        # print('ActionCards: {0}'.format(action_cards))
        # --------------------------------------------------------

        # Note: Goal cards are set up later below

        # --------------------------------------------------------
        # Nugget cards
        # --------------------------------------------------------
        nugget_deck = []
        one_nugget = 16
        two_nugget = 8
        three_nugget = 4
        for i in range(one_nugget):
            nugget_deck.append('1-Nugget')
        for i in range(two_nugget):
            nugget_deck.append('2-Nuggets')
        for i in range(three_nugget):
            nugget_deck.append('3-Nuggets')
        self._nugget_card_deck = nugget_deck
        # --------------------------------------------------------

        # --------------------------------------------------------
        # Combine path and action cards then shuffle
        # --------------------------------------------------------
        path_card_deck0 = path_card_deck.copy()
        action_card_deck0 = action_card_deck.copy()
        self._deck = path_card_deck0
        self._deck.extend(action_card_deck0)
        random.shuffle(self._deck)
        # --------------------------------------------------------

        # --------------------------------------------------------
        # Create reference decks #1
        # --------------------------------------------------------
        self._maindeck = {
            'PathCards': path_card_deck,
            'ActionCards': action_card_deck,
            'Deck': {'PathCards': path_card_deck, 'ActionCards': action_card_deck},
            'NuggetCards': nugget_deck,
            'DwarfCards': []
        }
        # print(self._maindeck)
        # --------------------------------------------------------

        # --------------------------------------------------------
        # Shuffle Nugget cards
        # --------------------------------------------------------
        random.shuffle(nugget_deck)
        # print(self.nugget_deck)
        # --------------------------------------------------------

        # --------------------------------------------------------
        # set decks to memory
        # --------------------------------------------------------
        self._nugget_deck = nugget_deck
        # --------------------------------------------------------

        # --------------------------------------------------------
        # Create reference decks #2
        # --------------------------------------------------------
        self._decks = {
            'Deck': self._deck,
            'Dwarf': [],
            'Nugget': self._nugget_deck
        }
        # --------------------------------------------------------

        # --------------------------------------------------------
        # SETTING UP BOARD
        # --------------------------------------------------------

        # setup board with initial placement cards
        # start card being the crossroad card with the ladder
        # and three goal cards
        start_card = PathCard.cross_road(special_card='start')
        goal_cards = []
        gold_idx = random.choice([0, 1, 2])
        for i in range(3):
            if gold_idx == i:
                label = 'gold'
            else:
                label = 'goal'
            goal_cards.append(label)

        # self._board.set_item_value(6, 10, 'start')
        self._board.set_item_value(0, 2, 'start')  # set start card location (y, x)
        self._path_list.append((0, 2))
        print(self._path_list)
        # self._board.set_item_value(6, 11, vertical)
        # print(self._board.get_item_value(6, 10))

        goal_locations = [(8, 0), (8, 2), (8, 4)]  # set goal card locations

        for i, goal in enumerate(goal_cards):
            self._board.set_item_value(goal_locations[i][0], goal_locations[i][1], goal)
        # print(self._board.get_item_value(14, 12))

        # add face down decks to board (non-playable area)
        self._board.set_item_value(0, 7, 'path_back')  # deck cards to draw from after turn taken
        self._board.set_item_value(1, 7, 'dwarf_back')  # deck card of left over dwarves
        self._board.set_item_value(2, 7, 'gold_back')  # deck cards of nuggets (offered to player at terminal state)

        # show map in terminal
        # print(self._board.get_map())
        # --------------------------------------------------------

        # --------------------------------------------------------
        # SETTING UP PLAYERS
        # --------------------------------------------------------

        """
        define players:
    
        3 players: 1 Saboteur and 3 Miners
        4 players: 1 Saboteur and 4 Miners
        5 players: 2 Saboteurs and 4 Miners
        6 players: 2 Saboteurs and 5 Miners
        7 players: 3 Saboteurs and 5 Miners
        8 players: 3 Saboteurs and 6 Miners
        9 players: 3 Saboteurs and 7 Miners
        10 players: 4 Saboteurs and 7 Miners
    
        define cards dealt:
    
        3 players: 6 cards each
        4 players: 6 cards each
        5 players: 6 cards each
        6 players: 5 cards each
        7 players: 5 cards each
        8 players: 4 cards each
        9 players: 4 cards each
        10 players: 4 cards each
        """

        print('Players being configured.')

        # dictionary to provide how many saboteurs, miners and cards each based on number of players
        players_dict = {
            3: {'Saboteur': 1, 'Miner': 3, 'Cards': 6},
            4: {'Saboteur': 1, 'Miner': 4, 'Cards': 6},
            5: {'Saboteur': 2, 'Miner': 4, 'Cards': 6},
            6: {'Saboteur': 2, 'Miner': 5, 'Cards': 5},
            7: {'Saboteur': 3, 'Miner': 5, 'Cards': 5},
            8: {'Saboteur': 3, 'Miner': 6, 'Cards': 4},
            9: {'Saboteur': 3, 'Miner': 7, 'Cards': 4},
            10: {'Saboteur': 4, 'Miner': 7, 'Cards': 4}
        }
        for num_players in players_dict:
            if nplayers == num_players:
                num_sabotuers = players_dict[num_players]['Saboteur']
                num_miners = players_dict[num_players]['Miner']
                cards_each = players_dict[num_players]['Cards']
        print('Number of players: {0}'.format(nplayers))
        print('Number of Saboteurs: {0}'.format(num_sabotuers))
        print('Number of Miners: {0}'.format(num_miners))
        print('Number of Cards each: {0}'.format(cards_each))

        # make a list of dwarf cards
        dwarf_card_deck = []
        for i in range(0, num_sabotuers):
            dwarf_card_deck.append('Saboteur')
        for j in range(0, num_miners):
            dwarf_card_deck.append('Miner')
        print('Combination of dwarfs: {0}'.format(dwarf_card_deck))
        random.shuffle(dwarf_card_deck)
        self._dwarf_card_deck = dwarf_card_deck
        self._decks.update({'Dwarf': dwarf_card_deck})
        self._maindeck.update({'DwarfCards': dwarf_card_deck})
        # print(self._decks['Dwarf'])
        # print(dwarf_card_deck)
        # print(self._maindeck)

        # --------------------------------------------------------
        # Create player list
        # --------------------------------------------------------
        player_list = []
        i = 1
        npl = int(nplayers)
        while i <= npl:
            player_list.append(i)
            i += 1
        # print(player_list) # [1, 2, 3]

        new_player_list = {}
        for i in range(1, npl + 1):
            key = i
            value = []
            new_player_list[key] = value
        print('Playerlist before: {0}'.format(new_player_list))

        actioncard_player_list = {}
        for i in range(1, npl + 1):
            key = i
            value = []
            actioncard_player_list[key] = value
        print('Actioncard Playerlist before: {0}'.format(actioncard_player_list))

        # create agent memory maps
        new_player_list2 = {}
        for i in range(1, npl + 1):
            key = i
            value = []
            new_player_list2[key] = value

        for i in range(1, npl + 1):
            key = i
            value = new_player_list2
            self.memory_map[key] = value
        print('Memory map dict: {0}'.format(self.memory_map))

        # --------------------------------------------------------

        # --------------------------------------------------------
        # Allocate dwarf cards to players
        # --------------------------------------------------------
        i = 1
        while i <= npl:
            sel_dwarf = dwarf_card_deck[i]
            update_val = {i: sel_dwarf}
            new_player_list.update(update_val)
            i += 1
        print('Playerlist after dwarf allocation: {0}'.format(new_player_list))
        self._players = new_player_list
        # --------------------------------------------------------

        # --------------------------------------------------------
        # Create Player hands - allocate cards to each player
        # --------------------------------------------------------
        all_items = self._deck
        # print(all_items)
        player_hand = {}
        for i in range(1, nplayers + 1):
            key = i
            value = []
            player_hand[key] = value
        print('Player hand before: {0}'.format(player_hand))

        print('Number of Cards in deck: {0}'.format(len(all_items)))

        for key in player_hand:
            for _ in range(cards_each):
                if all_items:
                    item = all_items.pop()
                    player_hand[key].append(item)

        self._player_hand = player_hand
        print('Player hand after card allocation: {0}'.format(player_hand))
        # --------------------------------------------------------

        # --------------------------------------------------------
        # Remaining cards in deck ready for future draws
        # --------------------------------------------------------
        self._remaining_cards = all_items
        print('Remaining cards in deck after player allocation: {0}'.format(len(all_items)))
        # --------------------------------------------------------

        # --------------------------------------------------------
        # Shuffle player list for turn taking order
        # --------------------------------------------------------
        player_turns = player_list.copy()
        random.shuffle(player_turns)
        print('Order of player turns: {0}'.format(player_turns))
        self._player_turns = player_turns
        # --------------------------------------------------------

        # --------------------------------------------------------
        # Take first player from the list as the starting player
        # --------------------------------------------------------
        starting_player = player_turns[0]
        self._player_turn = starting_player
        # --------------------------------------------------------

        self.main()

    # # get player turn
    # def turn(game_state):
    #     return game_state['player-turn']

    # Todo - In progress
    def _play_step(self):
        # get game state
        game_state = self.get_game_state()
        # check is terminal
        # if SaboteurGame.is_terminal(self, game_state):
        #    return

        """
        Who's turn is it?
        What cards do they have?
        What type of cards do they have?
        """
        cur_player = game_state['player-turn']  # 3
        print('Current Player turn: {0}'.format(cur_player))
        cur_agent = self._players[cur_player]  # Miner
        # cur_agent = type(SaboteurGame).turn(game_state)
        print('Current agent: {0}'.format(cur_agent))

        # --------------------------------------------------------
        # SENSE
        # Getting board, player, player hand information
        # to assist the AI to make card playing decisions
        # --------------------------------------------------------

        # self._agents[cur_agent].sense(SaboteurGame)
        # self._agents[cur_agent].sense(self)

        # print(game_state['game-board'].get_map())  # show map
        # print('Players hand:  {0}'.format(game_state['player-hand'][self._player_turn]))  # show player hand

        # Get player's hand and determine what card types they are (path or action)
        # print(SaboteurGame.get_player_hand(self, game_state))
        # hand = game_state['player-hand'][self._player_turn]
        hand = SaboteurGame.get_player_hand(self, game_state)
        print('Players hand:  {0}'.format(hand))  # show player hand

        options = {
            'Path': [],
            'Action': []
        }
        i = 0
        # print(len(hand))  # 6
        # print(game_state['path-card-deck'])
        while i <= len(hand) - 1:
            val = hand[i]
            if val in game_state['path-card-deck']:
                key = 'Path'
                options[key].append(val)
            elif val in game_state['action-card-deck']:
                key = 'Action'
                options[key].append(val)
            i += 1
        print('Player card options: {0}'.format(options))

        text = 'Player hand:'
        coords = (2, 8)
        self._draw_text(text, coords)

        self.draw_hand()

        # --------------------------------------------------------
        # THINK
        # researching the current game state to strategize card playing techniques
        # --------------------------------------------------------

        """
        need to think about how to look at the current board where paths are currently laid
        as a miner, goal is to reach the gold card hidden amongst the three goal cards
        and to assist other miners with mending when broken cards are given
        
        as a saboteur, same goal is to reach the gold, but also to provide broken cards to prevent miners
        
        """

        # actions = self._agents[cur_player].think()
        # player = 'Miner' if cur_player == 'Miner' else 'Saboteur'
        # player = player_turn
        # if len(actions) != 0:
        #     self._last_action = "{0} player played the move '{1}'".format(cur_player, actions[0])

        # --------------------------------------------------------
        # ACT
        # take action based on the strategy chosen
        # --------------------------------------------------------

        # self._agents[cur_player].act(actions)
        # self._board.set_item_value(1, 2, 'NEWC')
        # print(self._board.get_item_value(1,2))
        # pass
        # game_state = SaboteurGame.get_game_state()

        # --------------------------------------------------------
        # function testing playing a card chosen after AI think
        # --------------------------------------------------------
        ctype = 'Path'
        # ctype = 'Action'
        y = 3  # y coord
        x = 0  # x coord
        p = ''  # player to hand action card to
        card = random.choice(options[ctype])
        SaboteurGame.play_card(self, card, ctype, x, y, p)
        # --------------------------------------------------------

        SaboteurGame.next_player_turn(self, game_state)  # go to next player's turn

    def _reset_bg(self):
        self._display.fill(WHITE)

    # Todo - Complete - working
    # Draw card image references to board based on values on board
    def _draw_card(self, x, y, ttype, card):
        x_coord = self._padding_left + x * self._box_size
        y_coord = self._padding_top + y * self._box_size
        if ttype == 'blank':
            color = WHITE
            pygame.draw.rect(self._display, color, pygame.Rect(x_coord-1, y_coord-1, self._box_size, self._box_size), 1)
        elif ttype == 'card':
            color = BLACK
            pygame.draw.rect(self._display, color, pygame.Rect(x_coord-1, y_coord-1, self._box_size, self._box_size), 1)
            if card == 'start':
                self._display.blit(Deck.cards['wiki']['start'], (x_coord, y_coord))
            elif card == 'goal':
                self._display.blit(Deck.cards['wiki']['goal'], (x_coord, y_coord))
            else:
                self._display.blit(Deck.cards['wiki'][card], (x_coord, y_coord))

    # Todo - Complete - working
    # draw game board within pygame window
    def _draw_board(self):
        for i in range(0, self._n_cols):
            for j in range(0, self._n_rows):
                space = self._board.get_item_value(i, j)
                # print(space)
                if space is not None:
                    type = 'card'
                    self._draw_card(i, j, type, space)
                else:
                    if space == '?':
                        type = 'card'
                        card = 'goal'
                    else:
                        type = 'blank'
                        card = ''
                    self._draw_card(i, j, type, card)

    # draw text to pygame window
    def _draw_text(self, text_message, coords, font_size=20):
        x_coord = self._padding_left + coords[0] * self._box_size
        y_coord = self._padding_top + coords[1] * self._box_size

        pygame.draw.rect(self._display, BLACK, pygame.Rect(x_coord - 1, y_coord - 1, self._box_size, self._box_size), 1)

        font = pygame.font.Font(None, font_size)
        text = font.render(text_message, True, BLACK)
        self._display.blit(text, (x_coord, y_coord))
        pygame.display.flip()

    # Todo
    # draw game over within pygame window when there is a terminal state
    def _draw_game_over(self):
        pass

    # draw frame for pygame window
    def _draw_frame(self):
        self._reset_bg()
        self._draw_board()

    # suitable if there are human players
    def key_to_action(key):
        pass

    # suitable if there are human players
    def wait_for_user_input():
        pass

    # Todo - Completed - Working
    """
    current state of the game
    """
    def get_game_state(self):
        player_turn = self._player_turn  # what player turn is it?
        player_hand = self._player_hand  # what cards does the player hand have?
        remaining_cards = self._remaining_cards  # what cards are remaining in the draw deck?
        path_card_deck = self._path_card_deck  # get list of all path cards
        action_card_deck = self._action_card_deck  # get list of all action cards
        nugget_card_deck = self._nugget_card_deck  # get list of all nugget cards
        game_board = self._board.copy()  # get copy of game board
        player_turn_list = self._player_turns  # get player turn order list
        decks = self._decks
        path_list = self._path_list

        game_state = {
            'game-board': game_board,
            'player_turn_list': player_turn_list,
            'player-turn': player_turn,
            'player-hand': player_hand,
            'remaining-cards': remaining_cards,
            'decks': decks,
            'path-card-deck': path_card_deck,
            'action-card-deck': action_card_deck,
            'nugget-card-deck': nugget_card_deck,
            'path-list': path_list
        }
        return game_state

    # Todo - Completed - Working
    """
    function to rotate player turns when called after player card has been dealt
    """
    def next_player_turn(self, game_state):
        cur_player = game_state['player-turn']  # get current player
        # print(cur_player)
        player_turn_list = game_state['player_turn_list']  # get current turn list
        i = 0
        while i <= len(player_turn_list):
            if i == cur_player:  # when reach current player
                # print(player_turn_list)
                next_player_idx = player_turn_list.index(i) + 1  # get next player in list
                next_player = player_turn_list[next_player_idx]
                # print(next_player)
                player_turn_list = player_turn_list[1:] + player_turn_list[:1]  # shift list to left by 1
                self._player_turns = player_turn_list  # update player turn list
                self._player_turn = next_player  # update current player to next player
            i += 1

    # Todo - Completed - Working
    """
    show player's hand on screen
    """
    def draw_hand(self):
        col = 8
        game_state = self.get_game_state()
        player_hand = SaboteurGame.get_player_hand(self, game_state)
        if len(player_hand) <= 6:
            # text = str(player_hand[0])
            # self._draw_text(player_hand[0], (3, 7))
            self._board.set_item_value(3, col, player_hand[0])

            # self._draw_text(player_hand[1], (4, 7))
            self._board.set_item_value(4, col, player_hand[1])

            # self._draw_text(player_hand[2], (5, 7))
            self._board.set_item_value(5, col, player_hand[2])

            # self._draw_text(player_hand[3], (6, 7))
            self._board.set_item_value(6, col, player_hand[3])

            # self._draw_text(player_hand[4], (7, 7))
            self._board.set_item_value(7, col, player_hand[4])

            # self._draw_text(player_hand[5], (8, 7))
            self._board.set_item_value(8, col, player_hand[5])

    # Todo - Complete - Working
    # get current player's cards
    def get_player_hand(self, game_state):
        cur_player = game_state['player-turn']  # get current player
        player_hand = game_state['player-hand'][self._player_turn]
        return player_hand

    # Todo - Complete - Working
    # play a card from player's hand chosen by AI/human
    def play_card(self, card, ctype, x, y, player):
        game_state = self.get_game_state()
        # hand = SaboteurGame.get_player_hand(self, game_state)
        turn = game_state['player-turn']
        agent = self._players[turn]
        if ctype == 'Path':
            # validate then perform path card placement on board
            print('Player chose to place a path card {0}: '.format(card))
            self._board.set_item_value(x, y, card)  # place path card on board
            self._path_list.append((y, x))  # add path card to list
        elif ctype == 'Action':
            # validate then perform action card
            print('Player chose to present an action card {0} to player: {1} '.format(card, player))
            update_val = {player: card}
            self._action_given.update(update_val)
        self.remove_card(card)  # remove card from player's hand
        self.discard_card(card)  # discard card after it has been used
        self.draw_card(player)  # draw another card from the deck
        SaboteurGame.memorize(self, turn, agent, ctype, card)  # for each player, remember what card they played

    # Todo - Complete - Working
    def remove_card(self, card):
        game_state = self.get_game_state()
        player_hand = SaboteurGame.get_player_hand(self, game_state)
        player_hand.remove(card)
        print('Player hand after card removal: {0}'.format(player_hand))

    # Todo - Complete - Working
    def memorize(self, turn, agent, ctype, card):
        agent_memory = self.memory_map
        for turn_key in agent_memory:
            val = (ctype + '-' + card)
            if turn_key == turn:
                agent_memory[turn_key][turn_key].append(val)
        print('Agent memory map: {0}'.format(agent_memory))
        print('Memory map: {0}'.format(self.memory_map))

    # Todo - Complete - Working
    # add played card to discard deck
    def discard_card(self, card):
        self._discard_deck.append(card)
        print('Discard deck: {0}'.format(self._discard_deck))

    # Todo - Complete - Working
    # draw card from deck after player plays a card in hand
    def draw_card(self, player):
        if len(self._remaining_cards) > 0:
            game_state = self.get_game_state()
            player_hand = SaboteurGame.get_player_hand(self, game_state)
            print('Remaining cards from deck before draw: {0}'.format(self._remaining_cards))
            card = self._remaining_cards.pop()
            print('Card drawn from deck: {0}'.format(card))
            print('Remaining cards from deck after draw: {0}'.format(self._remaining_cards))
            player_hand.append(card)
        else:
            print('There are no more cards to draw from, deck empty.')

    # Todo
    # get winner
    def get_winner(game_state):
        game_board = game_state['game-board']
        winners = []
        if len(winners) == 1:
            return winners[0]
        else:
            return None

    # # get percepts for the AI agent
    # def get_percepts(self):
    #     game_state = self.get_game_state()
    #     return {
    #         'game-board-sensor': game_state['game-board'],
    #         'turn-taking-indicator': self._player_turn
    #     }

    # all sensors, actuators and actions defined here for the AI agent
    # Sensors
    # def add_all_sensors(self):
    #     self.add_sensor(
    #         sensor_name='game-board-sensor',
    #         initial_value=GridMap(0, 0, None),
    #         validation_function=lambda v: [None]
    #     )
    #     self.add_sensor(
    #         sensor_name='turn-taking-indicator',
    #         initial_value='Miner',
    #         validation_function=lambda v: v in ['Miner', 'Saboteur']
    #     )
    #     self.add_sensor(
    #         sensor_name='player-hand',
    #         initial_value=[],
    #         validation_function=lambda v: isinstance(v, list)
    #     )
    #
    # # Actuators
    # def add_all_actuators(self):
    #     self.add_actuator(
    #         actuator_name='play-hand',
    #         initial_value='path',
    #         validation_function=lambda v: v in SaboteurGame.play_hand
    #     )
    #
    # # Actions
    # def add_all_actions(self):
    #     for card in SaboteurGame.play_hand:
    #         self.add_action(
    #             'play-hand-{0}'.format(card),
    #             lambda c=card: {'play-hand': c}
    #        )

    # legal moves
    # ensure path cards to be playable are not illegal placements
    # def legal_moves(self):
    #     pass

    def transition_result(game_state, action):
        game_board = game_state['game-board'].copy()
        players = game_state['players']
        player_turn_list = game_state['player_turn_list']
        player_turn = game_state['player-turn']
        player_hand = game_state['player-hand'][player_turn]
        remaining_cards = game_state['remaining-cards']
        decks = game_state['decks']
        path_card_deck = game_state['path-card']
        action_card_deck = game_state['action-card']
        nugget_card_deck = game_state['nugget-card']
        path_list = game_state['path-list']

        new_game_state = {
            'game-board': game_board,
            'players': players,
            'player_turn_list': player_turn_list,
            'player-turn': player_turn,
            'player-hand': player_hand,
            'remaining-cards': remaining_cards,
            'decks': decks,
            'path-card': path_card_deck,
            'action-card': action_card_deck,
            'nugget-card': nugget_card_deck,
            'path-list': path_list
        }
        player_turn = game_state['player-turn']
        return new_game_state

    def state_transition(self, agent_actuators):
        action = None
        new_state = self.transition_result(self.get_game_state(), action)
        self._board = new_state['game-board'].copy()
        self._players = new_state['players']
        self._player_turns = new_state['player_turn_list']
        self._player_turn = new_state['player-turn']
        self._player_hand = new_state['player-hand']
        self._remaining_cards = new_state['remaining-cards']
        self._path_card_deck = new_state['path-card']
        self._action_card_deck = new_state['action-card']
        self._path_list = new_state['path-list']

    # Todo
    # players have cards and there are cards still in the facedown deck of path and action cards
    # legal moves should be what cards remain that can be considered a playable card
    def get_legal_actions(game_state):
        game_board = game_state['game-board']  # GridMap object
        player_turn = str(game_state['player-turn'])
        player_hand = str(game_state['player-hand'])
        board = game_state['game-board'].get_map()
        remaining_cards = str(game_state['remaining-cards'])
        path_card = str(game_state['path-card'])
        action_card = str(game_state['action-card'])
        path_list = game_state['path-list']

        legal_actions = []

        # Todo
        # based on player's hand, what path cards can they use on board

        # Todo
        # based on current state of game, can a player use an action card

        return legal_actions

    # Todo
    # When gamestate ends
    def is_terminal(game_state):
        remaining_actions = SaboteurGame.get_legal_actions(game_state)
        if len(remaining_actions) == 0:
            return True

        winner = SaboteurGame.get_winner(game_state)
        if winner is not None:
            return True

        return False

    # Todo
    # winner payoff
    def payoff(game_state, player):
        # it must return a payoff for the considered player ('Y' or 'R') in a given game_state
        winner = SaboteurGame.get_winner(game_state)
        print(winner)
        if winner is None:
            return 0
        elif winner == player:
            return 1
        else:
            return -1

    def main(self):
        running = True

        while running:
            # update frame
            self._draw_frame()
            pygame.display.update()
            self._window_clock.tick(1)
            # Event Tasking
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    quit()

            # updating game with one step
            # sense - think - act
            self._play_step()
            pygame.time.delay(2000)


if __name__ == '__main__':
    agent_miner = miner_behaviour
    agent_saboteur = saboteur_behaviour
    nplayers = 3

    SaboteurGame(agent_miner, agent_saboteur, nplayers)
