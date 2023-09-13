import random
from une_ai.models import Agent, GridMap
from deck import Deck

class SaboteurPlayer(Agent):
    play_hand = ['path', 'mend', 'sab', 'discard']

    # Constructor
    def __init__(self, agent_name, agent_program, players):
        super().__init__(agent_name, agent_program)
        self.name = agent_name
        self.hand = {}
        self.remaining_cards = []
        self.nplayers = players

    def set_players(nplayers):

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

        print('Players being configured.')

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

    def get_remaining_cards(self):
        pass
    def get_player(self, player):
        pass

    def get_nplayers(self, nplayers):
        return int(nplayers)

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
