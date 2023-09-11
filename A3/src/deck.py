from card import PathCard, ActionCard
import pygame
import random


# classic deck

# 27x action cards:
# 9x broken cards
# 3x pick axes
# 3x lanterns
# 3x mine carts

# 9x mend cards
# 2x pick axes
# 2x lanterns
# 2x mine carts
# 1x pick axe and mine cart combo
# 1x pick axe and lantern combo
# 1x lantern and mine cart combo

# 6x map cards
# 3x dynamite cards

# 28x Gold nugget cards:
# 4x 3 nuggets
# 8x 2 nuggets
# 16x 1 nugget

# 4x saboteurs
# 7x Gold Diggers

# 44x path cards:
# 1x starting card with ladder
# 4x south to north [|]
# 5x south to north, east [|-]
# 5x south to north, west to east [+]
# 5x west to east, north
# 3x west to east
# 4x south, east
# 5x south, west
# 1x south to mid
# 1x mid south, mid north
# 1x mid south, mid north, mid east
# 1x mid all
# 1x mid west, mid east, mid north
# 1x mid west, mid east
# 1x mid east, mid south
# 1x mid west, mid south
# 1x mid west

CARD_SIZE = (80, 80)


class Deck():
    def __init__(self):
        self._deck = [
            'E',
            'EW',
            'EWC',
            'N',
            'NE',
            'NEC',
            'NEW',
            'NEWC',
            'NS',
            'NSC',
            'NSE',
            'NSEC',
            'NSEW',
            'NSEWC',
            'NSW',
            'NSWC',
            'NW',
            'NWC',
            'S',
            'SE',
            'SEC',
            'SEW',
            'SEWC',
            'SW',
            'SWC',
            'W',
            'mend_lantcart',
            'mend_axelant',
            'mend_axecart',
            'mend_cart',
            'mend_axe',
            'mend_lant',
            'sab_axe',
            'sab_cart',
            'sab_lant',
            'map',
            'dynamite',
            None
        ]
        #self._initialise_deck()
        #self.shuffle()
        #self.card_reveal = False

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
            #if SaboteurGame.card_reveal:
            #    'gold': pygame.transform.scale(pygame.image.load('./Resources/GoalBack.jpg'), CARD_SIZE),
            #else:
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

    def _initialise_deck(self):

        # path cards
        for i in range(4):
            # self._deck.append(PathCard.vertical_tunnel())
            self._deck.append('NSC')

        for i in range(5):
            # self._deck.append(PathCard.vertical_junction())
            self._deck.append('NSEC')

        for i in range(5):
            # self._deck.append(PathCard.cross_road())
            self._deck.append('NSEWC')

        for i in range(5):
            # self._deck.append(PathCard.horizontal_junction())
            self._deck.append('NEWC')

        for i in range(3):
            # self._deck.append(PathCard.horizontal_tunnel())
            self._deck.append('EWC')

        for i in range(4):
            # self._deck.append(PathCard.turn())
            self._deck.append('NEC')

        for i in range(5):
            # self._deck.append(PathCard.reversed_turn())
            self._deck.append('NWC')

        # self._deck.append(PathCard.dead_end(['south']))
        self._deck.append('S')
        # self._deck.append(PathCard.dead_end(['north', 'south']))
        self._deck.append('NS')
        # self._deck.append(PathCard.dead_end(['north', 'east', 'south']))
        self._deck.append('NSE')
        # self._deck.append(PathCard.dead_end(['north', 'east', 'south', 'west']))
        self._deck.append('NSEW')
        # self._deck.append(PathCard.dead_end(['west', 'north', 'east']))
        self._deck.append('NEW')
        # self._deck.append(PathCard.dead_end(['west', 'east']))
        self._deck.append('EW')
        # self._deck.append(PathCard.dead_end(['south', 'east']))
        self._deck.append('SE')
        # self._deck.append(PathCard.dead_end(['south', 'west']))
        self._deck.append('SW')
        # self._deck.append(PathCard.dead_end(['west']))
        self._deck.append('W')

        # Action cards
        for i in range(6):
            self._deck.append(ActionCard('map'))

        for i in range(9):
            self._deck.append(ActionCard('sabotage'))

        for i in range(9):
            self._deck.append(ActionCard('mend'))

        for i in range(3):
            self._deck.append(ActionCard('dynamite'))

    # shuffle deck
    def shuffle(self):
        random.shuffle(self._deck)

    # draw from deck
    def draw(self):
        assert len(self._deck) > 0, "There are no more cards in the deck"

        return self._deck.pop()

    def get_deck(self):
        return self._deck
