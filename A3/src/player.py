from une_ai.models import Agent, GridMap
from deck import Deck

class Player(Agent):
    def __init__(self, name):
        self.name = name
        self.hand = {}

    def get_hand(self, name):
        return self.hand[name]

    # Sensors
    def add_all_sensors(self):
        self.add_sensor(
            'game-board-sensor',
            GridMap(0, 0, None),
            validation_function=lambda v: Deck.get_deck().copy()
        )

        self.add_sensor(
            'turn-taking-indicator',
            'Miner',
            lambda v: v in ['Miner', 'Saboteur']
        )

    # Actuators
    def add_all_actuators(self):
        self.add_actuator(
            'playcard',
            None,
            self.is_valid_card
        )

    # Actions
    def add_all_actions(self):
        pass