from card import PathCard, ActionCard
import random


class Deck():
    def __init__(self):
        self._deck = []

        self._initialise_deck()
        self.shuffle()

    def _initialise_deck(self):
        for i in range(4):
            self._deck.append(PathCard.vertical_tunnel())

        for i in range(5):
            self._deck.append(PathCard.vertical_junction())

        for i in range(5):
            self._deck.append(PathCard.cross_road())

        for i in range(5):
            self._deck.append(PathCard.horizontal_junction())

        for i in range(3):
            self._deck.append(PathCard.horizontal_tunnel())

        for i in range(4):
            self._deck.append(PathCard.turn())

        for i in range(5):
            self._deck.append(PathCard.reversed_turn())

        self._deck.append(PathCard.dead_end(['south']))
        self._deck.append(PathCard.dead_end(['north', 'south']))
        self._deck.append(PathCard.dead_end(['north', 'east', 'south']))
        self._deck.append(PathCard.dead_end(['north', 'east', 'south', 'west']))
        self._deck.append(PathCard.dead_end(['west', 'north', 'east']))
        self._deck.append(PathCard.dead_end(['west', 'east']))
        self._deck.append(PathCard.dead_end(['south', 'east']))
        self._deck.append(PathCard.dead_end(['south', 'west']))
        self._deck.append(PathCard.dead_end(['west']))

        for i in range(6):
            self._deck.append(ActionCard('map'))

        for i in range(9):
            self._deck.append(ActionCard('sabotage'))

        for i in range(9):
            self._deck.append(ActionCard('mend'))

        for i in range(3):
            self._deck.append(ActionCard('dynamite'))

    def shuffle(self):
        random.shuffle(self._deck)

    def draw(self):
        assert len(self._deck) > 0, "There are no more cards in the deck"

        return self._deck.pop()
