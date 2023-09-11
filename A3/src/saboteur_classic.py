import random
import pygame
import numpy as np

from une_ai.models import GridMap
from card import PathCard
from deck import Deck

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
NROWS = 5


class SaboteurGame:

    def __init__(self, agent_miner, agent_saboteur, players, display_w=DISPLAY_WIDTH,
                 display_h=DISPLAY_HEIGHT, box_size=BOX_SIZE):

        self._board = GridMap(NCOLS, NROWS, None)
        # self._player_turn = 'Miner'
        self._player_hand = {}
        self._remaining_cards = []

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

        self._agents = {}
        self._agents['Miner'] = agent_miner
        self._agents['Saboteur'] = agent_saboteur
        self._card_reveal = False

        #game_state = self._environment.get_game_state()
        #game_board = game_state['game-board']

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

        # vertical = PathCard.vertical_tunnel()
        # self._board.set_item_value(6, 10, 'start')
        self._board.set_item_value(0, 2, 'start')
        # self._board.set_item_value(6, 11, vertical)

        board = self._board
        # print(self._board.get_item_value(6, 10))
        goal_locations = [(8, 0), (8, 2), (8, 4)]

        for i, goal in enumerate(goal_cards):
            self._board.set_item_value(goal_locations[i][0], goal_locations[i][1], goal)
        # print(self._board.get_item_value(14, 12))

        # show map in terminal
        #print(self._board.get_map())

        # define players
        # 3 players: 1 Saboteur and 3 Miners
        # 4 players: 1 Saboteur and 4 Miners
        # 5 players: 2 Saboteurs and 4 Miners
        # 6 players: 2 Saboteurs and 5 Miners
        # 7 players: 3 Saboteurs and 5 Miners
        # 8 players: 3 Saboteurs and 6 Miners
        # 9 players: 3 Saboteurs and 7 Miners
        # 10 players: 4 Saboteurs and 7 Miners

        # define cards dealt
        # 3 players: 6 cards each
        # 4 players: 6 cards each
        # 5 players: 6 cards each
        # 6 players: 5 cards each
        # 7 players: 5 cards each
        # 8 players: 4 cards each
        # 9 players: 4 cards each
        # 10 players: 4 cards each

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
            if players == num_players:
                num_sabotuers = players_dict[num_players]['Saboteur']
                num_miners = players_dict[num_players]['Miner']
                cards_each = players_dict[num_players]['Cards']
        print('Number of players: {0}'.format(players))
        print('Number of Saboteurs: {0}'.format(num_sabotuers))
        print('Number of Miners: {0}'.format(num_miners))
        print('Number of Cards each: {0}'.format(cards_each))

        # make a list of dwarfs
        dwarf_list = []
        for i in range(0, num_sabotuers):
            dwarf_list.append('Saboteur')
        for j in range(0, num_miners):
            dwarf_list.append('Miner')
        print('Combination of dwarfs: {0}'.format(dwarf_list))

        player_list = []
        i = 1
        while i <= players + 1:
            player_list.append(i)
            i += 1
        #print(player_list)

        new_player_list = {}
        for i in range(1, players + 2):
            key = i
            value = []
            new_player_list[key] = value
        print('Playerlist before: {0}'.format(new_player_list))

        i = 1
        while i <= players + 1:
            # print(i)
            sel_rand_dwarf = random.choice(dwarf_list)
            # print(sel_rand_dwarf)
            dwarf_list.remove(sel_rand_dwarf)

            update_val = {i: sel_rand_dwarf}
            new_player_list.update(update_val)

            i += 1

        print('Playerlist after dwarf allocation: {0}'.format(new_player_list))

        # initialize deck
        # Deck._initialise_deck()
        # Deck()
        # cannot access Deck class with get_deck with self in it, manually creating it

        deck = []
        # path cards
        for i in range(4):
            deck.append('NSC')

        for i in range(5):
            deck.append('NSEC')

        for i in range(5):
            deck.append('NSEWC')

        for i in range(5):
            deck.append('NEWC')

        for i in range(3):
            deck.append('EWC')

        for i in range(4):
            deck.append('NEC')

        for i in range(5):
            deck.append('NWC')

        deck.append('S')
        deck.append('NS')
        deck.append('NSE')
        deck.append('NSEW')
        deck.append('NEW')
        deck.append('EW')
        deck.append('SE')
        deck.append('SW')
        deck.append('W')

        # Action cards
        for i in range(6):
            deck.append('map')

        for i in range(9):
            deck.append('sabotage')

        for i in range(9):
            deck.append('mend')

        for i in range(3):
            deck.append('dynamite')

        # hand out x cards to each player
        all_items = deck

        # print(all_items)
        # print(deck)
        player_hand = {}
        for i in range(1, players + 2):
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

        self._player_hand = player_hand
        print('Player hand after card allocation: {0}'.format(player_hand))

        self._remaining_cards = all_items
        print('Remaining cards in deck after player allocation: {0}'.format(len(all_items)))

        # shuffle players for turn taking order
        player_turns = player_list.copy()
        random.shuffle(player_turns)

        def rotate_turns(lst, n):
            n = n % len(player_turns)
            return lst[-n:] + lst[:-n]

        starting_player = rotate_turns(player_turns, 1)
        # print(rotate_turns[0])
        self._player_turn = starting_player

        self.main()

    def _play_step(self):
        # get game state
        #game_state = self._environment.get_game_state()
        # check is terminal
        #if type(self._environment).is_terminal(game_state):
        #    return



        # cur_player = SaboteurGame.turn(game_state)

        # SENSE
        # self._agents[cur_player].sense()
        # THINK
        # actions = self._agents[cur_player].think()
        # player = 'Miner' if cur_player == 'Miner' else 'Saboteur'
        # player = player_turn
        # if len(actions) != 0:
        #     self._last_action = "{0} player played the move '{1}'".format(cur_player, actions[0])
        # ACT
        # self._agents[cur_player].act(actions)
        self._board.set_item_value(1, 2, 'NEWC')
        # print(self._board.get_item_value(1,2))
        # pass

    def _reset_bg(self):
        self._display.fill(WHITE)

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
        pass

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

    # legal moves
    # players have cards and there are cards still in the facedown deck of path and action cards
    def legal_moves(self):
        pass

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

    nplayers = 3
    SaboteurGame(agent_miner, agent_saboteur, nplayers)  # how many players to pass in?
