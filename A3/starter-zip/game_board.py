from une_ai.models import GridMap
from card import PathCard
import random


class GameBoard():

    def __init__(self):
        self._board = GridMap(20, 20, None)

        start_card = PathCard.cross_road(special_card='start')
        goal_cards = []
        gold_idx = random.choice([0, 1, 2])
        for i in range(3):
            if gold_idx == i:
                label = 'gold'
            else:
                label = 'goal'
            goal_cards.append(PathCard.cross_road(special_card=label))

        self._board.set_item_value(6, 10, start_card)
        goal_locations = [(14, 8), (14, 10), (14, 12)]
        for i, goal in enumerate(goal_cards):
            self._board.set_item_value(goal_locations[i][0], goal_locations[i][1], goal)

    def get_board(self):
        return self._board.get_map()

    # TODO
    # This method does not check if there is a valid path from
    # the starting card to the new placed card
    def add_path_card(self, x, y, path_card):
        assert isinstance(path_card, PathCard), "The parameter path_card must be an instance of the class PathCard"
        assert x >= 0 and x < 20, "The x coordinate must be 0 <= x < 20"
        assert y >= 0 and y < 20, "The y coordinate must be 0 <= y < 20"
        assert self._board.get_item_value(x, y) is None, "There is already another card on the board at coordinates (" \
                                                         "{0}, {1})".format(x, y)

        self._board.set_item_value(x, y, path_card)

    def remove_path_card(self, x, y):
        assert x >= 0 and x < 20, "The x coordinate must be 0 <= x < 20"
        assert y >= 0 and y < 20, "The y coordinate must be 0 <= y < 20"
        assert self._board.get_item_value(x, y) is not None and not self._board.get_item_value(x, y).is_special_card(), \
            "There is no valid card to remove at coordinates ({0}, {1})".format(x, y)

        self._board.set_item_value(x, y, None)

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
