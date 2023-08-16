import random

from une_ai.models import Agent
from une_ai.models import GridMap

from une_ai.assignments.connect_four_base_environment import ConnectFourBaseEnvironment

class ConnectFourPlayer(Agent):
    decisionvalues = list(range(0, 7))
    # puvalues = list(range(, 7))
    decisiontype = ['release', 'popup']
    powerups = ['anvil', 'x2', 'wall', None]
    # powerups = ConnectFourBaseEnvironment.POWERUPS
    NCOLS = ConnectFourBaseEnvironment.N_COLS
    NROWS = ConnectFourBaseEnvironment.N_ROWS

    def __init__(self, agent_name, agent_program):
        super().__init__(agent_name, agent_program)

    # TODO
    # add all the necessary sensors as per the requirements
    def add_all_sensors(self):
        self.add_sensor(
            sensor_name='game-board-sensor',
            initial_value=GridMap(0, 0, None),
            validation_function=lambda v: ['Y', 'R', 'W', None]
        )
        self.add_sensor(
            sensor_name='powerups-sensor',
            # initial_value={'Y': [], 'R': []}
            initial_value={'Y': ConnectFourPlayer.powerups, 'R': ConnectFourPlayer.powerups},
            # validation_function= lambda v: {'Y': ConnectFourPlayer.powerups, 'R': ConnectFourPlayer.powerups}
            validation_function=lambda v: {'Y': self.powerups, 'R': self.powerups}
        )
        self.add_sensor(
            sensor_name='turn-taking-indicator',
            initial_value='Y',
            validation_function=lambda v: v in ['Y', 'R']
        )

    # TODO
    # add all the necessary actuators as per the requirements
    def add_all_actuators(self):
        self.add_actuator(
            actuator_name='checker-handler',
            initial_value=('release', 0),
            validation_function=lambda v: isinstance(v, tuple)
        )
        self.add_actuator(
            actuator_name='powerup-selector',
            initial_value=False,
            validation_function=lambda v: v in {False, True}
        )

    # TODO
    # add all the necessary actions as per the requirements

    def add_all_actions(self):
        for release in ConnectFourPlayer.decisionvalues:
            self.add_action(
                'release-{0}'.format(release),
                lambda r=release: {'checker-handler': ('release', r), 'powerup-selector': False}
            )
        for popup in ConnectFourPlayer.decisionvalues:
            self.add_action(
                'popup-{0}'.format(popup),
                lambda p=popup: {'checker-handler': ('popup', p), 'powerup-selector': False}
            )
        for powerup in ConnectFourPlayer.decisionvalues:
            self.add_action(
                'use-power-up-{0}'.format(powerup),
                lambda pu=powerup: {'checker-handler': ('release', pu), 'powerup-selector': True}  # if pu in range(0, 6) else {'powerup-selector': False}
            )
