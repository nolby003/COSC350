import pygame
import numpy as np

from deck import Deck

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


class SaboteurGame:

    def __init__(self, agent_miner, agent_saboteur, environment, players, display_w=DISPLAY_WIDTH,
                 display_h=DISPLAY_HEIGHT, box_size=BOX_SIZE):

        # pygame game window init and setup
        pygame.init()
        window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('Saboteur Card Game')
        window_clock = pygame.time.Clock()

        print('Saboteur Game loading.')

        self._box_size = box_size
        self._display = window
        self._window_clock = window_clock
        self._display_size = (display_w, display_h)
        self._agents = {'Miner': agent_miner, 'Saboteur': agent_saboteur}
        self._environment = environment
        self._last_action = ""

        game_state = self._environment.get_game_state()
        game_board = game_state['game-board']
        self._players = players

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

        self.main()

    def _play_step(self):
        game_state = self._environment.get_game_state()
        if type(self._environment).is_terminal(game_state):
            return

        cur_agent = type(self._environment).turn(game_state)
        # print(cur_player)
        # print(game_state['player-turn'])

        # SENSE
        self._agents[cur_agent].sense(self._environment)
        # THINK
        actions = self._agents[cur_agent].think()
        #print(actions)
        player = 'Miner' if cur_agent == 'Miner' else 'Saboteur'
        #if len(actions) != 0:
        #    self._last_action = "{0} player played the move '{1}'".format(player, actions[0])
        # ACT
        self._agents[cur_agent].act(actions, self._environment)

        board = game_state['game-board']
        board.set_item_value(1, 3, 'NEW')

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

    def key_to_action(key):
        pass

    def wait_for_user_input():
        pass

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
