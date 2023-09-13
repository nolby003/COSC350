# this version is all classes under one file

from une_ai.models import Agent
from une_ai.models import GridMap
from une_ai.models import GameEnvironment

from agent_programs import miner_behaviour, saboteur_behaviour

import random
import pygame
import numpy as np

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


# the core game functions
class SaboteurGame:

    def __init__(self, agent_miner, agent_saboteur, environment, players, display_w=DISPLAY_WIDTH,
                 display_h=DISPLAY_HEIGHT, box_size=BOX_SIZE):
        print('Saboteur Game loading.')
        # pygame game window init and setup
        pygame.init()
        window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('Saboteur Card Game')
        window_clock = pygame.time.Clock()

        self._box_size = box_size
        self._display = window
        self._window_clock = window_clock
        self._display_size = (display_w, display_h)
        self._agents = {'Miner': agent_miner, 'Saboteur': agent_saboteur}
        self._nplayers = players

        self._environment = environment
        self._last_action = ""

        game_state = self._environment.get_game_state()
        game_board = game_state['game-board']

        self._n_cols = game_board.get_width()
        self._n_rows = game_board.get_height()
        self._padding_left = int((self._display_size[0] - self._n_cols * self._box_size) / 2)
        self._padding_top = int((self._display_size[1] - self._n_rows * self._box_size) / 2)

        self._coordinates = np.array([[None] * self._n_cols] * self._n_rows)
        for y in range(self._n_rows):
            for x in range(self._n_cols):
                self._coordinates[y, x] = (x, y)

        fonts = pygame.font.get_fonts()
        self._font = fonts[0]  # default to a random font
        # try to look among the most common fonts
        test_fonts = ['arial', 'couriernew', 'verdana', 'helvetica', 'roboto']
        for font in test_fonts:
            if font in fonts:
                self._font = font
                break

        # setup players and create player hands
        SaboteurPlayer.set_players(self, self._nplayers)

        self.main()

    def _play_step(self):
        game_state = self._environment.get_game_state()
        #if type(self._environment).is_terminal(game_state):  # currently stopping the loop
        #    return

        cur_agent = type(self._environment).turn(game_state)
        print(cur_agent)
        #print('foo')
        # SENSE
        self._agents[cur_agent].sense(self._environment)
        # THINK
        actions = self._agents[cur_agent].think()
        print(actions)
        player = 'Miner' if cur_agent == 'Miner' else 'Saboteur'
        # if len(actions) != 0:
        #    self._last_action = "{0} player played the move '{1}'".format(player, actions[0])
        # ACT
        self._agents[cur_agent].act(actions, self._environment)

    def _reset_bg(self):
        self._display.fill(BLACK)

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

    def _draw_board(self):
        game_state = self._environment.get_game_state()
        game_board = game_state['game-board']
        for i in range(0, self._n_cols):
            for j in range(0, self._n_rows):
                space = game_board.get_item_value(i, j)
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

    def _draw_text(self, text_message, padding_top, orientation, font_size=20):
        font = pygame.font.SysFont(self._font, font_size)
        text_size = font.size(text_message)
        text = font.render(text_message, True, WHITE)
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

    def _draw_game_over(self):
        game_state = self._environment.get_game_state()
        game_board = game_state['game-board']
        player = type(self._environment).get_winner(game_state)
        if player == 'Miner':
            winner = 'Miners'
        elif player == 'Saboteur':
            winner = 'Saboteurs'
        else:
            winner = None

        # padding_top = INFO_BAR_HEIGHT
        # self._draw_text(text, padding_top, 'center')

    def _draw_frame(self):
        self._reset_bg()
        self._draw_board()
        # self._draw_text("Last action: {0}".format(self._last_action), POWERUPS_BAR_HEIGHT, 'left', 15)
        if type(self._environment).is_terminal(self._environment.get_game_state()):
            self._draw_game_over()
        else:
            colour = type(self._environment).turn(self._environment.get_game_state())
            # self._draw_text("Player Turn: {0}".format(player), 'left', 15)

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


# the groups and players of the game
class SaboteurPlayer(Agent):
    play_hand = ['path', 'mend', 'sab', 'discard']

    def __init__(self, agent_name, agent_program):
        super().__init__(agent_name, agent_program)

        print('Saboteur Players loading.')

    def set_players(self, nplayers):

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
        dwarf_list = []
        for i in range(0, num_sabotuers):
            dwarf_list.append('Saboteur')
        for j in range(0, num_miners):
            dwarf_list.append('Miner')
        print('Combination of dwarfs: {0}'.format(dwarf_list))

        player_list = []
        i = 1
        while i <= nplayers + 1:
            player_list.append(i)
            i += 1
        # print(player_list) # [1, 2, 3, 4]

        new_player_list = {}
        for i in range(1, nplayers + 2):
            key = i
            value = []
            new_player_list[key] = value
        print('Playerlist before: {0}'.format(new_player_list))

        # shuffle dwarf list amongst players
        i = 1
        while i <= nplayers + 1:
            # print(i)
            sel_rand_dwarf = random.choice(dwarf_list)
            # print(sel_rand_dwarf)
            dwarf_list.remove(sel_rand_dwarf)

            update_val = {i: sel_rand_dwarf}
            new_player_list.update(update_val)

            i += 1

        print('Playerlist after dwarf allocation: {0}'.format(new_player_list))

        all_items = Deck.set_decks()

        # print(all_items[0])

        player_hand = {}
        for i in range(1, nplayers + 2):
            key = i
            value = []
            player_hand[key] = value
        print('Player hand before: {0}'.format(player_hand))

        print('Number of Cards in deck: {0}'.format(len(all_items)))
        print('Deck before shuffle: {0}'.format(all_items))
        random.shuffle(all_items)
        print('Deck after shuffle: {0}'.format(all_items))

        for key in player_hand:
            for _ in range(cards_each):
                if all_items:
                    item = all_items.pop()
                    player_hand[key].append(item)

        # player_hand = player_hand
        print('Player hand after card allocation: {0}'.format(player_hand))

        remaining_cards = all_items
        print('Remaining cards in deck after player allocation: {0}'.format(len(remaining_cards)))

        # shuffle players for turn taking order
        player_turns = player_list.copy()
        random.shuffle(player_turns)
        print('Current Player: {0}'.format(player_turns[0]))

    def get_hand(player):
        pass

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
            validation_function=lambda v: v in SaboteurPlayer.play_hand
        )

    # Actions
    def add_all_actions(self):
        for card in SaboteurPlayer.play_hand:
            self.add_action(
                'play-hand-{0}'.format(card),
                lambda c=card: {'play-hand': c}
            )


# the core base game environment
class SaboteurBaseEnvironment(GameEnvironment):
    N_COLS = 9
    N_ROWS = 5

    def __init__(self):
        super().__init__("Saboteur Game Environment")

        # setup game board
        self._board = GridMap(SaboteurBaseEnvironment.N_COLS, SaboteurBaseEnvironment.N_ROWS, None)
        board = self._board
        self._player_turn = 'Miner'

        print('Saboteur Game Environment loading.')

        # define goal cards
        goal_cards = []
        gold_idx = random.choice([0, 1, 2])
        for i in range(3):
            if gold_idx == i:
                label = 'gold'
            else:
                label = 'goal'
            goal_cards.append(label)

        # place start card on board
        self._board.set_item_value(0, 2, 'start')

        # place goal cards on board
        goal_locations = [(8, 0), (8, 2), (8, 4)]
        for i, goal in enumerate(goal_cards):
            self._board.set_item_value(goal_locations[i][0], goal_locations[i][1], goal)

        # print(self._board.get_map())  # works
        # self._board.set_item_value(1, 2, 'NEWC')  # works
        # game_state = self.get_game_state()
        # print(game_state['game-board'].get_map())

    def add_player(self, player):
        if len(self._players) == 0:
            player = 'Miner'
        else:
            player = 'Saboteur'
        self._players[player] = player
        return player

    def get_game_state(self):
        player_turn = self._player_turn
        # player_hand = SaboteurPlayer.get_hand()
        # remaining_cards = Deck.get_deck()
        game_state = {
            'game-board': self._board.copy(),
            'players': self._players,
            'player-turn': player_turn,
            # 'player-hand': player_hand,
            # 'remaining-cards': remaining_cards
        }
        return game_state

    def get_legal_actions(game_state):
        game_board = game_state['game-board']  # GridMap object
        players = game_state['players']
        player_turn = str(game_state['player-turn'])
        # player_hand = str(game_state['player-hand'])
        board = game_state['game-board'].get_map()
        # remaining_cards = str(game_state['remaining-cards'])

        legal_actions = []
        player_cards = []
        # for val in player_hand[1]:
        #     player_cards.append(val)
        # legal_actions = player_cards
        # legal_actions.extend(remaining_cards)
        # print(legal_actions)
        return legal_actions

    # When gamestate ends
    def is_terminal(game_state):
        remaining_actions = SaboteurBaseEnvironment.get_legal_actions(game_state)
        if len(remaining_actions) == 0:
            return True

        winner = SaboteurBaseEnvironment.get_winner(game_state)
        if winner is not None:
            return True

        return False

    def get_player_name(self, marker):
        pass

    def get_winner(game_state):
        game_board = game_state['game-board']
        winners = []
        if len(winners) == 1:
            return winners[0]
        else:
            return None

    def turn(game_state):
        return game_state['player-turn']

    def transition_result(game_state, action):
        game_board = game_state['game-board'].copy()
        players = game_state['players']
        player_turn = game_state['player-turn']
        #player_hand = game_state['player-hand']
        #remaining_cards = game_state['remaining-cards']

        new_game_state = {
            'game-board': game_board,
            'players': players,
            'player-turn': player_turn,
            #'player-hand': player_hand,
            #'remaining-cards': remaining_cards
        }

        player_turn = game_state['player-turn']

        #if action.startswith('player-hand-'):
        #    pass

        return new_game_state

    # winner payoff
    def payoff(game_state, player):
        # it must return a payoff for the considered player ('Y' or 'R') in a given game_state
        winner = SaboteurBaseEnvironment.get_winner(game_state)
        # print(winner)
        if winner is None:
            return 0
        elif winner == player:
            return 1
        else:
            return -1

    def get_percepts(self):
        game_state = self.get_game_state()
        return {
            'game-board-sensor': game_state['game-board'],
            'turn-taking-indicator': self._player_turn
        }

    def state_transition(self, agent_actuators):
        action = None
        new_state = SaboteurBaseEnvironment.transition_result(self.get_game_state(), action)
        self._board = new_state['game-board'].copy()
        #self._player_turn = new_state['player-turn']
        #self._player_hand = new_state['player-hand']
        #self._remaining_cards = new_state['remaining-cards']


CARD_SIZE = (80, 80)


# defines card decks for the game
# functions to check and retrieve
class Deck:
    def __init__(self):
        self._deck = []

        print('Saboteur Deck loading.')

    # card images
    cards = {
        'Original': {
            'path_back': pygame.transform.scale(pygame.image.load('./Resources/PathBack.jpg'), CARD_SIZE),
            'start': pygame.transform.scale(pygame.image.load('./Resources/StartCard.jpg'), CARD_SIZE),
            'goal': pygame.transform.scale(pygame.image.load('./Resources/GoalBack.jpg'), CARD_SIZE),
            'gold': pygame.transform.scale(pygame.image.load('./Resources/GOLD.jpg'), CARD_SIZE),
            'E': pygame.transform.scale(pygame.image.load('./Resources/PathCards/E.jpg'), CARD_SIZE),
            'EW': pygame.transform.scale(pygame.image.load('./Resources/PathCards/EW.jpg'), CARD_SIZE),
            'EWC': pygame.transform.scale(pygame.image.load('./Resources/PathCards/EWC.jpg'), CARD_SIZE),
            'N': pygame.transform.scale(pygame.image.load('./Resources/PathCards/N.jpg'), CARD_SIZE),
            'NE': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NE.jpg'), CARD_SIZE),
            'NEC': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NEC.jpg'), CARD_SIZE),
            'NEW': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NEW.jpg'), CARD_SIZE),
            'NEWC': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NEWC.jpg'), CARD_SIZE),
            'NS': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NS.jpg'), CARD_SIZE),
            'NSC': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NSC.jpg'), CARD_SIZE),
            'NSE': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NSE.jpg'), CARD_SIZE),
            'NSEC': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NSEC.jpg'), CARD_SIZE),
            'NSEW': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NSEW.jpg'), CARD_SIZE),
            'NSEWC': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NSEW.jpg'), CARD_SIZE),
            'NSW': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NSW.jpg'), CARD_SIZE),
            'NSWC': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NSWC.jpg'), CARD_SIZE),
            'NW': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NW.jpg'), CARD_SIZE),
            'NWC': pygame.transform.scale(pygame.image.load('./Resources/PathCards/NWC.jpg'), CARD_SIZE),
            'S': pygame.transform.scale(pygame.image.load('./Resources/PathCards/S.jpg'), CARD_SIZE),
            'SE': pygame.transform.scale(pygame.image.load('./Resources/PathCards/SE.jpg'), CARD_SIZE),
            'SEC': pygame.transform.scale(pygame.image.load('./Resources/PathCards/SEC.jpg'), CARD_SIZE),
            'SEW': pygame.transform.scale(pygame.image.load('./Resources/PathCards/SEW.jpg'), CARD_SIZE),
            'SEWC': pygame.transform.scale(pygame.image.load('./Resources/PathCards/SEWC.jpg'), CARD_SIZE),
            'SW': pygame.transform.scale(pygame.image.load('./Resources/PathCards/SW.jpg'), CARD_SIZE),
            'SWC': pygame.transform.scale(pygame.image.load('./Resources/PathCards/SWC.jpg'), CARD_SIZE),
            'W': pygame.transform.scale(pygame.image.load('./Resources/PathCards/W.jpg'), CARD_SIZE),
            'coal': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/Coal.jpg'), CARD_SIZE),

            'mend_lantcart': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/mjHgzhM_07.jpg'),
                                                    CARD_SIZE),
            'mend_axelant': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/mjHgzhM_14.jpg'),
                                                   CARD_SIZE),
            'mend_axecart': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/mjHgzhM_21.jpg'),
                                                   CARD_SIZE),
            'mend_cart': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/mjHgzhM_27.jpg'),
                                                CARD_SIZE),
            'mend_axe': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/mjHgzhM_63.jpg'), CARD_SIZE),
            'mend_lant': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/mjHgzhM_62.jpg'),
                                                CARD_SIZE),
            'sab_axe': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/mjHgzhM_42.jpg'), CARD_SIZE),
            'sab_cart': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/mjHgzhM_06.jpg'), CARD_SIZE),
            'sab_lant': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/mjHgzhM_41.jpg'), CARD_SIZE),
            'map': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/mjHgzhM_43.jpg'), CARD_SIZE),
            'dynamite': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/mjHgzhM_28.jpg'), CARD_SIZE),
            # '3_goldnugg': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/'), CARD_SIZE),
            # '2_goldnugg': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/'), CARD_SIZE),
            # '1_goldnugg': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/'), CARD_SIZE),
            'saboteur': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/Saboteur.jpg'), CARD_SIZE),
            'miner': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/GoldDigger.jpg'), CARD_SIZE)
        },
        'wiki': {
            'path_back': pygame.transform.scale(pygame.image.load('./Resources/PathBack.jpg'), CARD_SIZE),
            'start': pygame.transform.scale(pygame.image.load('./wiki_resources/start.png'), CARD_SIZE),
            'goal': pygame.transform.scale(pygame.image.load('./Resources/GoalBack.jpg'), CARD_SIZE),
            # if SaboteurGame.card_reveal:
            #    'gold': pygame.transform.scale(pygame.image.load('./Resources/GoalBack.jpg'), CARD_SIZE),
            # else:
            #    'gold': pygame.transform.scale(pygame.image.load('./Resources/GOLD.jpg'), CARD_SIZE),
            'gold': pygame.transform.scale(pygame.image.load('./Resources/GoalBack.jpg'), CARD_SIZE),
            'E': pygame.transform.scale(pygame.image.load('./wiki_resources/E.png'), CARD_SIZE),
            'EW': pygame.transform.scale(pygame.image.load('./wiki_resources/EW.png'), CARD_SIZE),
            'EWC': pygame.transform.scale(pygame.image.load('./wiki_resources/EWC.png'), CARD_SIZE),
            'N': pygame.transform.scale(pygame.image.load('./wiki_resources/N.png'), CARD_SIZE),
            'NE': pygame.transform.scale(pygame.image.load('./wiki_resources/NE.png'), CARD_SIZE),
            'NEC': pygame.transform.scale(pygame.image.load('./wiki_resources/NEC.png'), CARD_SIZE),
            'NEW': pygame.transform.scale(pygame.image.load('./wiki_resources/NEW.png'), CARD_SIZE),
            'NEWC': pygame.transform.scale(pygame.image.load('./wiki_resources/NEWC.png'), CARD_SIZE),
            'NS': pygame.transform.scale(pygame.image.load('./wiki_resources/NS.png'), CARD_SIZE),
            'NSC': pygame.transform.scale(pygame.image.load('./wiki_resources/NSC.png'), CARD_SIZE),
            'NSE': pygame.transform.scale(pygame.image.load('./wiki_resources/NSE.png'), CARD_SIZE),
            'NSEC': pygame.transform.scale(pygame.image.load('./wiki_resources/NSEC.png'), CARD_SIZE),
            'NSEW': pygame.transform.scale(pygame.image.load('./wiki_resources/NSEW.png'), CARD_SIZE),
            'NSEWC': pygame.transform.scale(pygame.image.load('./wiki_resources/NSEWC.png'), CARD_SIZE),
            'NSW': pygame.transform.scale(pygame.image.load('./wiki_resources/NSW.png'), CARD_SIZE),
            'NSWC': pygame.transform.scale(pygame.image.load('./wiki_resources/NSWC.png'), CARD_SIZE),
            'NW': pygame.transform.scale(pygame.image.load('./wiki_resources/NW.png'), CARD_SIZE),
            'NWC': pygame.transform.scale(pygame.image.load('./wiki_resources/NWC.png'), CARD_SIZE),
            'S': pygame.transform.scale(pygame.image.load('./wiki_resources/S.png'), CARD_SIZE),
            'SE': pygame.transform.scale(pygame.image.load('./wiki_resources/SE.png'), CARD_SIZE),
            'SEC': pygame.transform.scale(pygame.image.load('./wiki_resources/SEC.png'), CARD_SIZE),
            'SEW': pygame.transform.scale(pygame.image.load('./wiki_resources/SEW.png'), CARD_SIZE),
            'SEWC': pygame.transform.scale(pygame.image.load('./wiki_resources/SEWC.png'), CARD_SIZE),
            'SW': pygame.transform.scale(pygame.image.load('./wiki_resources/SW.png'), CARD_SIZE),
            'SWC': pygame.transform.scale(pygame.image.load('./wiki_resources/SWC.png'), CARD_SIZE),
            'W': pygame.transform.scale(pygame.image.load('./wiki_resources/W.png'), CARD_SIZE),

            'coal': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/Coal.jpg'), CARD_SIZE),
            'mend_lantcart': pygame.transform.scale(pygame.image.load('./wiki_resources/mend_cartlant.png'),
                                                    CARD_SIZE),
            'mend_axelant': pygame.transform.scale(pygame.image.load('./wiki_resources/mend_lantaxe.png'),
                                                   CARD_SIZE),
            'mend_axecart': pygame.transform.scale(pygame.image.load('./wiki_resources/mend_axecart.png'),
                                                   CARD_SIZE),
            'mend_cart': pygame.transform.scale(pygame.image.load('./wiki_resources/mend_cart.png'),
                                                CARD_SIZE),
            'mend_axe': pygame.transform.scale(pygame.image.load('./wiki_resources/mend_axe.png'), CARD_SIZE),
            'mend_lant': pygame.transform.scale(pygame.image.load('./wiki_resources/mend_lant.png'),
                                                CARD_SIZE),
            'sab_axe': pygame.transform.scale(pygame.image.load('./wiki_resources/sab_axe.png'), CARD_SIZE),
            'sab_cart': pygame.transform.scale(pygame.image.load('./wiki_resources/sab_cart.png'), CARD_SIZE),
            'sab_lant': pygame.transform.scale(pygame.image.load('./wiki_resources/sab_lant.png'), CARD_SIZE),
            'map': pygame.transform.scale(pygame.image.load('./wiki_resources/map.png'), CARD_SIZE),
            'dynamite': pygame.transform.scale(pygame.image.load('./wiki_resources/dynamite.png'), CARD_SIZE),
            # '3_goldnugg': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/'), CARD_SIZE),
            # '2_goldnugg': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/'), CARD_SIZE),
            # '1_goldnugg': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/'), CARD_SIZE),
            'saboteur': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/Saboteur.jpg'), CARD_SIZE),
            'miner': pygame.transform.scale(pygame.image.load('./Resources/SpecialCards/GoldDigger.jpg'), CARD_SIZE)
        }
    }

    def set_decks():

        print('Deck being configured.')

        path_card_deck = []
        # path cards
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

        action_card_deck = []
        # Action cards
        for i in range(6):
            action_card_deck.append('map')

        for i in range(9):
            action_card_deck.append('sabotage')

        for i in range(9):
            action_card_deck.append('mend')

        for i in range(3):
            action_card_deck.append('dynamite')

        # hand out x cards to each player
        all_items = path_card_deck
        all_items.extend(action_card_deck)

        return all_items

    # shuffle deck
    def shuffle(self):
        random.shuffle(self._deck)

    # draw from deck
    def draw(self):
        assert len(self._deck) > 0, "There are no more cards in the deck"

        return self._deck.pop()

    def get_deck(self):
        return self._deck


class Card:
    def __init__(self, card_type, image):
        self.card_type = card_type
        self.image = image


class ActionCard(Card):

    def __init__(self, action):
        assert action in ['map', 'sabotage', 'mend', 'dynamite'], "The parameter action must be either map, sabotage, " \
                                                                  "mend or dynamite"

        self._action = action

    def get_action(self):
        return self._action


class InvalidTunnel(Exception):
    pass


class PathCard(Card):

    def __init__(self, tunnels, special_card=None):
        assert isinstance(tunnels, list), "The parameter tunnels must be a list of tuples"
        assert special_card in ['start', 'goal', 'gold', None], "The parameter special_card must be either None, " \
                                                                "start, goal or gold"

        for tunnel in tunnels:
            if not self._is_valid_tunnel(tunnel):
                raise InvalidTunnel("The tunnel '{0}' is an invalid one for this card.".format(tunnel))

        self._special_card = special_card
        self._revealed = False
        if special_card:
            # special cards are all cross roads
            cross_road = PathCard.cross_road()
            self._tunnels = cross_road.get_tunnels()
            if special_card in ['goal', 'gold']:
                self._revealed = False
        else:
            self._tunnels = tunnels

    def cross_road(special_card=None):
        return PathCard(
            [
                ('north', 'south'),
                ('north', 'east'),
                ('north', 'west'),
                ('south', 'east'),
                ('south', 'west'),
                ('east', 'west')
            ], special_card=special_card
            # return PathCard.pathcard['startcard']
        )

    def vertical_tunnel():
        return PathCard(
            [
                ('north', 'south')
            ]
        )

    def horizontal_tunnel():
        return PathCard(
            [
                ('east', 'west')
            ]
        )

    def vertical_junction():
        return PathCard(
            [
                ('north', 'south'),
                ('north', 'east'),
                ('south', 'east')
            ]
        )

    def horizontal_junction():
        return PathCard(
            [
                ('east', 'north'),
                ('west', 'north'),
                ('east', 'west')
            ]
        )

    def turn():
        return PathCard(
            [
                ('south', 'east')
            ]
        )

    def reversed_turn():
        return PathCard(
            [
                ('south', 'west')
            ]
        )

    def dead_end(directions):
        tunnels = []
        for direction in directions:
            tunnels.append((direction, None))
        return PathCard(tunnels)

    def _is_valid_tunnel(self, tunnel):
        if not isinstance(tunnel, tuple):
            return False
        if len(tunnel) != 2:
            return False
        for direction in tunnel:
            if direction not in ['north', 'east', 'south', 'west', None]:
                return False
        if tunnel[0] is None:
            return False
        if tunnel[0] is None and tunnel[1] is None:
            return False
        if tunnel[0] == tunnel[1]:
            return False

        return True

    def is_special_card(self):
        return self._special_card is not None

    def is_gold(self):
        return self._special_card == 'gold'

    def reveal_card(self):
        self._revealed = True

    def turn_card(self):
        tunnels = []
        opposite = {
            'north': 'south',
            'east': 'west',
            'west': 'east',
            'south': 'north',
        }
        for tunnel in self._tunnels:
            new_tunnel = (
                opposite[tunnel[0]] if tunnel[0] is not None else None,
                opposite[tunnel[1]] if tunnel[1] is not None else None
            )
            tunnels.append(new_tunnel)

        self._tunnels = tunnels

    def get_tunnels(self):
        return self._tunnels.copy()

    def __str__(self):
        # print('foo')
        card_rep = ['   ', '   ', '   ']
        if self._revealed:
            for tunnel in self._tunnels:
                directions = [(tunnel[0], tunnel[1]), (tunnel[1], tunnel[0])]
                for direction in directions:
                    tunnel_from = direction[0]
                    tunnel_to = direction[1]
                    if tunnel_from == 'north':
                        card_rep[0] = card_rep[0][:1] + '|' + card_rep[0][2:]
                        if tunnel_to is not None:
                            card_rep[1] = card_rep[1][:1] + '┼' + card_rep[1][2:]
                    elif tunnel_from == 'south':
                        card_rep[2] = card_rep[2][:1] + '|' + card_rep[2][2:]
                        if tunnel_to is not None:
                            card_rep[1] = card_rep[1][:1] + '┼' + card_rep[1][2:]
                    elif tunnel_from == 'east':
                        card_rep[1] = card_rep[1][:2] + '—'
                        if tunnel_to is not None:
                            card_rep[1] = card_rep[1][:1] + '┼' + card_rep[1][2:]
                    elif tunnel_from == 'west':
                        card_rep[1] = '—' + card_rep[1][1:]
                        if tunnel_to is not None:
                            card_rep[1] = card_rep[1][:1] + '┼' + card_rep[1][2:]
        else:
            return '   \n ? \n   '
        return '\n'.join(card_rep)


# the execution of the game


class SaboteurApp:

    def __init__(self):
        if __name__ == '__main__':
            nplayers = 3

            agent_miner = SaboteurPlayer('Miner', miner_behaviour)
            agent_saboteur = SaboteurPlayer('Saboteur', saboteur_behaviour)

            environment = SaboteurBaseEnvironment()
            environment.add_player(agent_miner)
            environment.add_player(agent_saboteur)

            SaboteurGame(agent_miner, agent_saboteur, environment, nplayers)


SaboteurApp()
