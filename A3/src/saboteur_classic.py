import random
import pygame
import numpy as np
from une_ai.models import GridMap
from card import PathCard

BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (125, 125, 125)
BLUE = (10, 20, 200)
GREEN = (255, 125, 125)

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
BOX_SIZE = 60

NCOLS = 20
NROWS = 20


class SaboteurGame:

    def __init__(self, players, display_w=DISPLAY_WIDTH,
                 display_h=DISPLAY_HEIGHT, box_size=BOX_SIZE):

        self._board = GridMap(NCOLS, NROWS, None)

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
        self._padding_left = int((self._display_size[0] - NCOLS*self._box_size)/2)
        self._padding_top = int((self._display_size[1] - NCOLS*self._box_size)/2)

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

        start_card = PathCard.cross_road(special_card='start')
        goal_cards = []
        gold_idx = random.choice([0, 1, 2])
        for i in range(3):
            if gold_idx == i:
                label = 'gold'
            else:
                label = 'goal'
            goal_cards.append(PathCard.cross_road(special_card=label))

        vertical = PathCard.vertical_tunnel()
        self._board.set_item_value(6, 10, start_card)
        self._board.set_item_value(6, 11, vertical)

        print(self._board.get_map())
        board = self._board
        # print(self._board.get_item_value(6, 11))
        goal_locations = [(14, 8), (14, 10), (14, 12)]
        for i, goal in enumerate(goal_cards):
            self._board.set_item_value(goal_locations[i][0], goal_locations[i][1], goal)

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
        while i <= players+1:
            player_list.append(i)
            i += 1
        print(player_list)

        new_player_list = {}
        keys = player_list
        new_player_list = dict(zip(keys, [None]*len(player_list)))
        print('Playerlist before: {0}'.format(new_player_list))

        player_list = random.shuffle

        i = 1
        while i <= players+1:
            # print(i)
            sel_rand_dwarf = random.choice(dwarf_list)
            # print(sel_rand_dwarf)
            dwarf_list.remove(sel_rand_dwarf)

            update_val = {i: sel_rand_dwarf}
            new_player_list.update(update_val)

            i += 1

        print('Playerlist after: {0}'.format(new_player_list))

        # print(PathCard.get_tunnels())

        self.main()

    def _play_step(self):
        pass

    def _reset_bg(self):
        self._display.fill(WHITE)

    def _draw_card(self, x, y, ttype):
        if ttype == 'blank':
            color = WHITE
        else:
            color = BLUE
        x_coord = self._padding_left + x * self._box_size
        y_coord = self._padding_top + y * self._box_size
        pygame.draw.rect(self._display, color, pygame.Rect(x_coord, y_coord, self._box_size, self._box_size))

    # draw game board within pygame window
    def _draw_board(self):
        for i in range(0, self._n_cols):
            for j in range(0, self._n_rows):
                if self._board.get_item_value(i, j) is not None:
                    type = 'card'
                    self._draw_card(i, j, type)
                else:
                    type = 'blank'
                    self._draw_card(i, j, type)

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
            # self._play_step()


if __name__ == '__main__':
    SaboteurGame(3)  # how many players to pass in?
