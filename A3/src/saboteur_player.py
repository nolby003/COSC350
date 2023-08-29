import random

from une_ai.models import Agent
from une_ai.models import GridMap

from saboteur_base_environment import SaboteurBaseEnvironment



class SaboteurPlayer(Agent):
    # define number of players and build list
    # dynamic so that you can extend or reduce amount of players
    numPlayers = 8
    playerList = []
    count = 0
    while count <= numPlayers:
        playerList.append('Player'.format(count))
        count += 1

    # define player groups
    player_groups = ['Gold-Diggers', 'Saboteurs']

    # Constructor
    def __init__(self, agent_name, agent_program):
        super().__init__(agent_name, agent_program)

    # Sensors
    def add_all_sensors(self):
        self.add_sensor(
            sensor_name='',
            initial_value='',
            validation_function=''
        )

    # Actuators
    def add_all_actuators(self):
        self.add_actuator(
            actuator_name='',
            initial_value='',
            validation_function=''
        )

    # Actions
    def add_all_actions(self):
        pass
