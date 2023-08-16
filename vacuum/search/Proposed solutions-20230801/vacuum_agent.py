# THIS CODE IS GIVEN TO YOU
# YOU DO NOT NEED TO EDIT THIS CODE
from une_ai.models import Agent

class VacuumAgent(Agent):

    WHEELS_DIRECTIONS = ['north', 'south', 'west', 'east']

    def __init__(self, agent_program):
        super().__init__(
            agent_name='vacuum_agent',
            agent_program=agent_program
        )
        
    def add_all_sensors(self):
        self.add_sensor('battery-level', 0, lambda v: isinstance(v, float) or isinstance(v, int) and v >= 0)
        self.add_sensor('location-sensor', (0, 0), lambda v: isinstance(v, tuple) and isinstance(v[0], int) and isinstance(v[1], int))

        directions = VacuumAgent.WHEELS_DIRECTIONS.copy()
        directions.append('center')
        for direction in directions:
            self.add_sensor('dirt-sensor-{0}'.format(direction), False, lambda v: v in [True, False])
            if direction != 'center':
                self.add_sensor('bumper-sensor-{0}'.format(direction), False, lambda v: v in [True, False])
    
    def add_all_actuators(self):
        self.add_actuator(
            'wheels-direction',
            'north',
            lambda v: v in VacuumAgent.WHEELS_DIRECTIONS
        )
        self.add_actuator(
            'vacuum-power',
            0,
            lambda v: v in [0, 1]
        )
        self.add_actuator(
            'suction-power',
            0,
            lambda v: v in [0, 1]
        )

    def add_all_actions(self):
        self.add_action(
            'start-cleaning',
            lambda: {'vacuum-power': 1} if not self.is_out_of_charge() else {}
        )
        self.add_action(
            'stop-cleaning',
            lambda: {
                'vacuum-power': 0
            }
        )
        self.add_action(
            'activate-suction-mechanism',
            lambda: {'suction-power': 1} if not self.is_out_of_charge() else {}
        )
        self.add_action(
            'deactivate-suction-mechanism',
            lambda: {
                'suction-power': 0
            }
        )
        for direction in VacuumAgent.WHEELS_DIRECTIONS:
            self.add_action(
                'change-direction-{0}'.format(direction),
                lambda d=direction: {'wheels-direction': d} if not self.is_out_of_charge() else {}
            )

    def get_pos_x(self):
        return self.read_sensor_value('location-sensor')[0]
    
    def get_pos_y(self):
        return self.read_sensor_value('location-sensor')[1]
    
    def is_out_of_charge(self):
        return self.read_sensor_value('battery-level') == 0
    
    def get_battery_level(self):
        return int(self.read_sensor_value('battery-level'))
    
    def collision_detected(self):
        directions = VacuumAgent.WHEELS_DIRECTIONS.copy()
        for direction in directions:
            bumper = self.read_sensor_value('bumper-sensor-{0}'.format(direction))
            if bumper:
                return direction
        
        return None

    def did_collide(self):
        return False if self.collision_detected() is None else True