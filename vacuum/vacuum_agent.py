from une_ai.models import Agent

class VacuumAgent(Agent):

    WHEELS_DIRECTIONS = ['north', 'south', 'west', 'east']

    def __init__(self, agent_program):
        super().__init__(
            agent_name='vacuum_agent',
            agent_program=agent_program
        )
        
    # TODO: add all the sensors
    def add_all_sensors(self):
        self.add_sensor(
            sensor_name='location-sensor',
            initial_value=(0,0),
            validation_function=lambda value: isinstance(value,tuple) and len(value) == 2 and isinstance(value[0],int) and isinstance(value[1],int)
        )
        self.add_sensor('battery-level', 0, lambda v: isinstance(v, float) or isinstance(v, int) and v >= 0)
        directions = VacuumAgent.WHEELS_DIRECTIONS.copy()
        directions.append('center')
        for direction in directions:
            self.add_sensor('dirt-sensor-{0}'.format(direction), False, lambda v: v in [True, False])
            if direction != 'center':
                self.add_sensor('bumper-sensor-{0}'.format(direction), False, lambda v: v in [True, False])


    # TODO: add all the actuators
    def add_all_actuators(self):
        self.add_actuator(
            actuator_name='wheels-direction',
            initial_value='north',
            validation_function=lambda value: value in VacuumAgent.WHEELS_DIRECTIONS
        )

        self.add_actuator(
            actuator_name='vacuum-power',
            initial_value=0,
            validation_function=lambda value: value in [0, 1]
        )

        self.add_actuator(
            actuator_name='suction-power',
            initial_value=0,
            validation_function=lambda value: value in [0, 1]
        )

    # TODO: add all the actions
    def add_all_actions(self):
        self.add_action(
            action_name='start-cleaning',
            action_function=lambda: {'vacuum-power': 1} if not self.is_out_of_charge() else {}
        )

        self.add_action(
            action_name='stop-cleaning',
            action_function=lambda: {'vacuum-power': 0}
        )

        self.add_action(
            action_name='activate-suction-mechanism',
            action_function=lambda: {'suction-power': 1} if not self.is_out_of_charge() else {}
        )

        self.add_action(
            action_name='deactivate-suction-mechanism',
            action_function=lambda: {'suction-power': 0}
        )

        for direction in VacuumAgent.WHEELS_DIRECTIONS:
            self.add_action(
                'change-direction-{0}'.format(direction),
                lambda d=direction: {'wheels-direction': d} if not self.is_out_of_charge() else {}
            )
    # TODO: implement the following methods

    def get_pos_x(self):
        # It must return the x coord of the agent 
        # based on the location-sensor value
        return self.read_sensor_value('location-sensor')[0]
    
    def get_pos_y(self):
        # It must return the y coord of the agent 
        # based on the location-sensor value
        return self.read_sensor_value('location-sensor')[1]
    
    def get_battery_level(self):
        # It must return the rounded (as int) sensory value 
        # from the sensor battery-level
        return int(self.read_sensor_value('battery-level'))
    
    def is_out_of_charge(self):
        # It must return True if the sensor battery-level
        # is 0 and False otherwise
        return self.read_sensor_value('battery-level') == 0
    
    def collision_detected(self):
        # It must return the direction of the bumper
        # sensor collided with a wall if any, or None otherwise
        directions = VacuumAgent.WHEELS_DIRECTIONS.copy()
        for direction in directions:
            bumper = self.read_sensor_value('bumper-sensor-{0}'.format(direction))
            if bumper:
                return direction

        return None

    # This function is already implemented
    # so you do not need to change it
    def did_collide(self):
        return False if self.collision_detected() is None else True