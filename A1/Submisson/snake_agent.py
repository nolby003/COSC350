from une_ai.models import Agent
from une_ai.assignments import SnakeGame

class SnakeAgent(Agent):

    # snake directions
    SNAKE_DIRECTIONS = ['up', 'down', 'left', 'right']
    # snake eat status - mouth
    SNAKE_EAT_STATUS = ['open', 'close']

    # DO NOT CHANGE THE PARAMETERS OF THIS METHOD
    def __init__(self, agent_program):
        # DO NOT CHANGE THE FOLLOWING LINES OF CODE
        super().__init__("Snake Agent", agent_program)

        """
        If you need to add more instructions
        in the constructor, you can add them here
        """

    """
    TODO:
    In order for the agent to gain access to all 
    the sensors specified in the assignment's 
    requirements, it is essential to implement 
    this method.
    You can add a single sensor with the method:
    self.add_sensor(sensor_name, initial_value, validation_function)
    """

    def add_all_sensors(self):
        # body-sensor
        self.add_sensor(
            sensor_name='body-sensor',
            initial_value=[(0, 0)],
            validation_function=lambda value: isinstance(value, list)
        )
        # food-sensor
        self.add_sensor(
            sensor_name='food-sensor',
            initial_value=[(0, 0, 0)],
            validation_function=lambda value: isinstance(value, list)
        )
        # obstacles-sensor
        self.add_sensor(
            sensor_name='obstacles-sensor',
            initial_value=[(0, 0)],
            validation_function=lambda value: isinstance(value, list)
        )
        # clock
        self.add_sensor(
            sensor_name='clock',
            initial_value=60,
            validation_function=lambda value: isinstance(value, int) and value >= 0
        )

    """
    TODO:
    In order for the agent to gain access to all 
    the actuators specified in the assignment's 
    requirements, it is essential to implement 
    this method.
    You can add a single actuator with the method:
    self.add_actuator(actuator_name, initial_value, validation_function)
    """

    def add_all_actuators(self):
        # head
        self.add_actuator(
            actuator_name='head',
            initial_value='down',
            validation_function=lambda value: value in SnakeAgent.SNAKE_DIRECTIONS
        )
        # mouth
        self.add_actuator(
            actuator_name='mouth',
            initial_value='close',
            validation_function=lambda value: value in SnakeAgent.SNAKE_EAT_STATUS
        )

    """
    TODO:
    In order for the agent to gain access to all 
    the actions specified in the assignment's 
    requirements, it is essential to implement 
    this method.
    You can add a single action with the method:
    self.add_action(action_name, action_function)
    """

    def add_all_actions(self):
        # change direction of snake
        for direction in SnakeAgent.SNAKE_DIRECTIONS:
            self.add_action(
                'change-direction-{0}'.format(direction),
                lambda d=direction: {'head': d}
            )
            self.add_action(
                'move-{0}'.format(direction),
                lambda d=direction: {'head': d}
            )
        # change mouth open or close
        for eatstatus in SnakeAgent.SNAKE_EAT_STATUS:
            # open-mouth
            self.add_action(
                '{0}-mouth'.format(eatstatus),
                lambda s=eatstatus: {'mouth': s}
            )