import pygame
import numpy as np

BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (125, 125, 125)
BLUE = (10, 20, 200)
GREEN = (255, 125, 125)

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 500
POWERUPS_BAR_HEIGHT = 35
SCORE_BAR_HEIGHT = 35
INFO_BAR_HEIGHT = 35
BOX_SIZE = 20


class SaboteurGame:

    def __init__(self, environment, display_w=DISPLAY_WIDTH, display_h=DISPLAY_HEIGHT, box_size=BOX_SIZE):
        # assert type(environment).__name__ == 'SaboteurEnvironment', "environment must be an instance of a subclass " \
                                                                       # "of the class SaboteurBaseEnvironment"

        pygame.init()
        window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT+SCORE_BAR_HEIGHT))
        pygame.display.set_caption('Saboteur')
        window_clock = pygame.time.Clock()

        self._box_size = box_size
        self._display = window
        self._window_clock = window_clock
        self._display_size = (display_w, display_h)
        self._agents = {}
        self._environment = environment

        game_state = self._environment.get_game_state()
        game_board = game_state['game-board']

        self._n_cols = game_board.get_width()
        self._n_rows = game_board.get_height()
        self._padding_left = int((self._display_size[0] - self._n_cols*self._box_size)/2)
        self._padding_top = int((self._display_size[1] - self._n_rows*self._box_size)/2)

        self._coordinates = np.array([[None]*self._n_cols]*self._n_rows)
        for y in range(self._n_rows):
            for x in range(self._n_cols):
                self._coordinates[y, x] = (x, y)

        fonts = pygame.font.get_fonts()
        self._font = fonts[0] # default to a random font
        # try to look among the most common fonts
        test_fonts = ['arial', 'couriernew', 'verdana', 'helvetica', 'roboto']
        for font in test_fonts:
            if font in fonts:
                self._font = font
                break

        self.main()

    def _play_step(self):
        pass

    def _reset_bg(self):
        self._display.fill(BLACK)

    def _draw_board(self):
        pass

    def _draw_text(self, text_message, padding_top, orientation, font_size = 20):
        font = pygame.font.SysFont(self._font, font_size)
        text_size = font.size(text_message)
        text = font.render(text_message, True, WHITE)
        top = self._padding_top + self._n_rows*self._box_size + 10 + padding_top
        if orientation == 'center':
            left = int((self._display_size[0] - text_size[0])/2)
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
        # colour = type(self._environment).get_winner(game_state)
        # if colour == 'Y':
        #     winner = 'Yellow player'
        # elif colour == 'R':
        #     winner = 'Red player'
        # else:
        #     winner = None

        # if winner is not None:
        #     text = "{0} won!".format(winner)
        # else:
        #     text = "Tie!"

        # padding_top = POWERUPS_BAR_HEIGHT + INFO_BAR_HEIGHT
        # self._draw_text(text, padding_top, 'center')

    def _draw_frame(self):
        self._reset_bg()
        self._draw_board()
        # self._draw_powerups()
        # self._draw_text("Last action: {0}".format(self._last_action), POWERUPS_BAR_HEIGHT, 'left', 15)
        if type(self._environment).is_terminal(self._environment.get_game_state()):
            self._draw_game_over()
        else:
            colour = type(self._environment).turn(self._environment.get_game_state())
            player = "Yellow" if colour == 'Y' else "Red"
            self._draw_text("Player Turn: {0}".format(player), POWERUPS_BAR_HEIGHT + INFO_BAR_HEIGHT, 'left', 15)

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

            # if self._is_debugging:
            #     pygame.time.delay(2000)