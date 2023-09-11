import random

import numpy as np
from scipy.signal import convolve2d, convolve

from une_ai.models import GameEnvironment
from une_ai.models import GridMap

from card import PathCard
from deck import Deck


class InvalidMoveException(Exception):
    pass


class SaboteurBaseEnvironment(GameEnvironment):
    N_COLS = 9
    N_ROWS = 5

    def __init__(self):
        super().__init__("Saboteur Game Environment")
        self._board = GridMap(SaboteurBaseEnvironment.N_COLS, SaboteurBaseEnvironment.N_ROWS, None)
        self._player_turn = 'Miner'
        # self._players = 3
        self._playerss = 3

        print('Saboteur Game Environment loading.')

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
        # print(self._board.get_map())

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
            if self._playerss == num_players:
                num_sabotuers = players_dict[num_players]['Saboteur']
                num_miners = players_dict[num_players]['Miner']
                cards_each = players_dict[num_players]['Cards']
        print('Number of players: {0}'.format(self._players))
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
        while i <= self._playerss + 1:
            player_list.append(i)
            i += 1
        # print(player_list)

        new_player_list = {}
        for i in range(1, self._playerss + 2):
            key = i
            value = []
            new_player_list[key] = value
        print('Playerlist before: {0}'.format(new_player_list))

        i = 1
        while i <= self._playerss + 1:
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
        for i in range(1, self._playerss + 2):
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
        print('Current Player: {0}'.format(self._player_turn))

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

    def add_player(self, player):
        if len(self._players) == 0:
            player = 'Y'
        else:
            player = 'R'
        self._players[player] = player
        return player

    def get_game_state(self):
        game_state = {
            'game-board': self._board.copy(),
            'players': self._playerss,
            'player-turn': self._player_turn,
            'player-hand': self._player_hand,
            'remaining-cards': self._remaining_cards
        }
        return game_state

    def turn(game_state):
        return game_state['player-turn']

    def get_winner(game_state):
        game_board = game_state['game-board']
        winners = []
        if len(winners) == 1:
            return winners[0]
        else:
            return None

    def get_percepts(self):
        game_state = self.get_game_state()
        return {
            'game-board-sensor': game_state['game-board'],
            'turn-taking-indicator': self._player_turn
        }

    def _change_player_turn(self):
        self._prev_turn = self._player_turn
        if self._player_turn == 'Miner':
            self._player_turn = 'Saboteur'
        else:
            self._player_turn = 'Miner'

    def transition_result(game_state, action):
        game_board = game_state['game-board'].copy()
        players = game_state['players']
        player_turn = game_state['player-turn']
        player_hand = game_state['player-hand']
        remaining_cards = game_state['remaining-cards']

        new_game_state = {
            'game-board': game_board,
            'players': players,
            'player-turn': player_turn,
            'player-hand': player_hand,
            'remaining-cards': remaining_cards
        }

        player_turn = game_state['player-turn']

        return new_game_state

    def state_transition(self, agent_actuators):
        action = None
        new_state = SaboteurBaseEnvironment.transition_result(self.get_game_state(), action)
        self._board = new_state['game-board'].copy()
        self._player_turn = new_state['player-turn']
        self._player_hand = new_state['player-hand']
        self._remaining_cards = new_state['remaining-cards']
