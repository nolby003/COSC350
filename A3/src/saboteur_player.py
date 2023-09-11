import random
from une_ai.models import Agent, GridMap

from A3.src import deck
from saboteur_base_environment import SaboteurBaseEnvironment


class SaboteurPlayer(Agent):

    play_hand = ['path', 'mend', 'sab', 'discard']

    # Constructor
    def __init__(self, agent_name, agent_program):
        super().__init__(agent_name, agent_program)

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
