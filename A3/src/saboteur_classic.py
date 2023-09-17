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
NROWS = 8


class SaboteurGame():
    play_hand = ['path', 'mend', 'sab', 'discard']

    def __init__(self, agent_miner, agent_saboteur, nplayers, display_w=DISPLAY_WIDTH, display_h=DISPLAY_HEIGHT
                 , box_size=BOX_SIZE):

        self._board = GridMap(NCOLS, NROWS, None)
        self._player_turn = None
        self._player_hand = {}

        self._remaining_cards = []
        self._deck = []
        self._decks = {}

        self._nplayers = nplayers
        self._players = {}
        self._player_turns = []

        self._dwarf_card_deck = []
        self._action_card_deck = []
        self._path_card_deck = []
        self._nugget_card_deck = []

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
        for i in range(9):
            action_card_deck.append('sabotage')
        for i in range(9):
            action_card_deck.append('mend')
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
        self._board.set_item_value(0, 2, 'start')  # set start card location
        # self._board.set_item_value(6, 11, vertical)
        # print(self._board.get_item_value(6, 10))

        goal_locations = [(8, 0), (8, 2), (8, 4)]  # set goal card locations

        for i, goal in enumerate(goal_cards):
            self._board.set_item_value(goal_locations[i][0], goal_locations[i][1], goal)
        # print(self._board.get_item_value(14, 12))

        # add face down decks to board (non-playable area)
        self._board.set_item_value(2, 7, 'path_back')  # deck cards to draw from after turn taken

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

    # get player turn
    def turn(game_state):
        return game_state['player-turn']

    def _play_step(self):
        # get game state
        game_state = self.get_game_state()
        # check is terminal
        #if type(self._environment).is_terminal(game_state):
        #    return

        cur_player = game_state['player-turn']  # 3
        print('Current Player turn: {0}' .format(cur_player))
        cur_agent = self._players[cur_player]  # Miner
        # cur_agent = type(SaboteurGame).turn(game_state)
        print('Current agent: {0}'.format(cur_agent))

        # --------------------------------------------------------
        # SENSE
        # --------------------------------------------------------
        # self._agents[cur_agent].sense(SaboteurGame)
        # self._agents[cur_agent].sense(self)

        #print(game_state['game-board'].get_map())  # show map
        print('Players hand:  {0}'.format(game_state['player-hand'][self._player_turn]))  # show player hand

        # need to check each card in player's hand to determine card type
        # perhaps by a function
        hand = game_state['player-hand'][self._player_turn]
        options = {
            'Path': [],
            'Action': []
        }
        i = 0
        #print(len(hand))  # 6
        #print(game_state['path-card-deck'])
        while i <= len(hand)-1:
            val = hand[i]
            if val in game_state['path-card-deck']:
                key = 'Path'
                options[key].append(val)
            elif val in game_state['action-card-deck']:
                key = 'Action'
                options[key].append(val)
            i += 1
        print('Player card options: {0}'.format(options))

        # --------------------------------------------------------
        # THINK
        # --------------------------------------------------------
        # actions = self._agents[cur_player].think()
        # player = 'Miner' if cur_player == 'Miner' else 'Saboteur'
        # player = player_turn
        # if len(actions) != 0:
        #     self._last_action = "{0} player played the move '{1}'".format(cur_player, actions[0])

        # --------------------------------------------------------
        # ACT
        # --------------------------------------------------------
        # self._agents[cur_player].act(actions)
        # self._board.set_item_value(1, 2, 'NEWC')
        # print(self._board.get_item_value(1,2))
        # pass

    def _reset_bg(self):
        self._display.fill(WHITE)

    # Draw card image references to board based on values on board
    def _draw_card(self, x, y, ttype, card):
        x_coord = self._padding_left + x * self._box_size
        y_coord = self._padding_top + y * self._box_size
        if ttype == 'blank':
            color = WHITE
            pygame.draw.rect(self._display, color, pygame.Rect(x_coord, y_coord, self._box_size, self._box_size))
        elif ttype == 'card':
            color = BLUE
            pygame.draw.rect(self._display, color, pygame.Rect(x_coord, y_coord, self._box_size, self._box_size))
            if card == 'start':
                self._display.blit(Deck.cards['wiki']['start'], (x_coord, y_coord))
            elif card == 'goal':
                self._display.blit(Deck.cards['wiki']['goal'], (x_coord, y_coord))
            else:
                self._display.blit(Deck.cards['wiki'][card], (x_coord, y_coord))

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
    def _draw_text(self, text_message, padding_top, orientation, font_size=20):
        font = pygame.font.SysFont(self._font, font_size)
        text_size = font.size(text_message)
        text = font.render(text_message, True, BLACK)
        top = self._padding_top + self._n_rows * self._box_size + 10 + padding_top
        if orientation == 'center':
            left = int((self._display_size[0] - text_size[0]) / 2)
        elif orientation == 'left':
            left = self._padding_left
        elif orientation == 'right':
            left = self._display_size[0] - text_size[0] - self._padding_left
        else:
            left = 0
        self._display.blit(text, (left, top))

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

    # current state of the game
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

        game_state = {
            'game-board': game_board,
            'player_turn_list': player_turn_list,
            'player-turn': player_turn,
            'player-hand': player_hand,
            'remaining-cards': remaining_cards,
            'decks': decks,
            'path-card-deck': path_card_deck,
            'action-card-deck': action_card_deck,
            'nugget-card-deck': nugget_card_deck
        }
        return game_state

    # Todo
    # function to rotate player turns when called after player card has been dealt
    def next_player_turn(player):
        pass

    # Todo
    # show players hand on screen
    def draw_hand(player):
        pass

    # Todo
    # get current player's cards
    def get_player_hand(self, player):
        return self._player_hand[self._player_turn]

    # Todo
    # play a card from player's hand
    def play_card(self, player):
        cards = []
        cards = self.get_player_hand(player)
        for card in cards:
            print(card)

    # Todo
    # draw card from deck after player plays a card in hand
    def draw_card(player):
        pass



    # get winner
    def get_winner(game_state):
        game_board = game_state['game-board']
        winners = []
        if len(winners) == 1:
            return winners[0]
        else:
            return None

    # get percepts for the AI agent
    def get_percepts(self):
        game_state = self.get_game_state()
        return {
            'game-board-sensor': game_state['game-board'],
            'turn-taking-indicator': self._player_turn
        }

    # all sensors, actuators and actions defined here for the AI agent
    # Sensors
    def add_all_sensors(self):
        self.add_sensor(
            sensor_name='game-board-sensor',
            initial_value=GridMap(0, 0, None),
            validation_function=lambda v: [None]
        )
        self.add_sensor(
            sensor_name='turn-taking-indicator',
            initial_value='Miner',
            validation_function=lambda v: v in ['Miner', 'Saboteur']
        )
        self.add_sensor(
            sensor_name='player-hand',
            initial_value=[],
            validation_function=lambda v: isinstance(v, list)
        )

    # Actuators
    def add_all_actuators(self):
        self.add_actuator(
            actuator_name='play-hand',
            initial_value='path',
            validation_function=lambda v: v in SaboteurGame.play_hand
        )

    # Actions
    def add_all_actions(self):
        for card in SaboteurGame.play_hand:
            self.add_action(
                'play-hand-{0}'.format(card),
                lambda c=card: {'play-hand': c}
            )

    # Todo
    # legal moves
    # ensure path cards to be playable are not illegal placements
    def legal_moves(self):
        pass

    def transition_result(game_state, action):
        game_board = game_state['game-board'].copy()
        players = game_state['players']
        player_turn = game_state['player-turn']
        print(player_turn)
        player_hand = game_state['player-hand'][player_turn]
        remaining_cards = game_state['remaining-cards']
        path_card_deck = game_state['path-card']
        action_card_deck = game_state['action-card']

        new_game_state = {
            'game-board': game_board,
            'players': players,
            'player-turn': player_turn,
            'player-hand': player_hand,
            'remaining-cards': remaining_cards,
            'path-card': path_card_deck,
            'action-card': action_card_deck
        }

        player_turn = game_state['player-turn']

        #if action.startswith('player-hand-'):
        #    pass

        return new_game_state

    def state_transition(self, agent_actuators):
        action = None
        new_state = self.transition_result(self.get_game_state(), action)
        self._board = new_state['game-board'].copy()
        self._player_turn = new_state['player-turn']
        self._player_hand = new_state['player-hand']
        self._remaining_cards = new_state['remaining-cards']
        self._path_card_deck = new_state['path-card']
        self._action_card_deck = new_state['action-card']

    # Todo
    # players have cards and there are cards still in the facedown deck of path and action cards
    # legal moves should be what cards remain that can be considered a playable card
    def get_legal_actions(game_state):
        game_board = game_state['game-board']  # GridMap object
        players = game_state['players']
        player_turn = str(game_state['player-turn'])
        player_hand = str(game_state['player-hand'])
        board = game_state['game-board'].get_map()
        remaining_cards = str(game_state['remaining-cards'])
        path_card = str(game_state['path-card'])
        action_card = str(game_state['action-card'])

        legal_actions = []
        player_cards = []
        for val in player_hand[1]:
            player_cards.append(val)
        legal_actions = player_cards
        legal_actions.extend(remaining_cards)
        # print(legal_actions)
        return legal_actions

    # When gamestate ends
    def is_terminal(game_state):
        remaining_actions = SaboteurGame.get_legal_actions(game_state)
        if len(remaining_actions) == 0:
            return True

        winner = SaboteurGame.get_winner(game_state)
        if winner is not None:
            return True

        return False

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

    def __str__(self):
        no_card = '   \n   \n   '
        board_map = self._board.get_map()
        board_str = ''
        for row in board_map:
            for i in range(3):
                for card in row:
                    if card is None:
                        board_str += no_card.split('\n')[i]
                    else:
                        board_str += str(card).split('\n')[i]
                board_str += '\n'

        return board_str

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

    @property
    def card_reveal(self):
        return self._card_reveal


if __name__ == '__main__':
    agent_miner = miner_behaviour
    agent_saboteur = saboteur_behaviour
    # environment = SaboteurBaseEnvironment()
    # environment.add_player('Miner', agent_miner)
    # environment.add_player('Saboteur', agent_saboteur)

    nplayers = 3
    SaboteurGame(agent_miner, agent_saboteur, nplayers)
