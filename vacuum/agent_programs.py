import math
import random
import numpy as np

from une_ai.vacuum import DISPLAY_HEIGHT, DISPLAY_WIDTH, TILE_SIZE
from une_ai.models import GridMap
from vacuum_agent import VacuumAgent

DIRECTIONS = VacuumAgent.WHEELS_DIRECTIONS

"""
Test agent:
- If the vacuum power is off, it starts cleaning
- At each time, it chooses a random direction for the wheels
"""


def test_behaviour(percepts, actuators):
    actions = []

    if actuators['vacuum-power'] != 1:
        actions.append('start-cleaning')
    new_direction = random.choice(DIRECTIONS)
    actions.append('change-direction-{0}'.format(new_direction))

    return actions


"""
Simple reflex agent: 
- If the vacuum power is off, it starts cleaning
- If there is dirt on the current tile (i.e. 'dirt-sensor-center'), 
it activates the suction mechanism
- If the agent hits a wall, it changes the direction of the wheels randomly
- If the agent senses dirt on the surrounding tiles, 
it changes the direction of the wheels towards the dirt
"""


def simple_reflex_behaviour(percepts, actuators):
    actions = []



    # if the power is off we start cleaning
    if actuators['vacuum-power'] != 1:
        actions.append('start-cleaning')

    # if there is dirt, we activate the suction mechanism
    if percepts['dirt-sensor-center'] == True:
        actions.append('activate-suction-mechanism')
    elif actuators['suction-power'] == 1:
        # if not and the suction mechanism is on, we shut it down to conserve battery
        actions.append('deactivate-suction-mechanism')

    cur_direction = actuators['wheels-direction']
    new_direction = cur_direction

    print(percepts['bumper-sensor-{0}'.format(cur_direction)])

    # if we bumped into a wall we change direction
    if percepts['bumper-sensor-{0}'.format(cur_direction)] == True:
        directions = DIRECTIONS.copy()
        # we remove the current direction from the list
        directions.remove(cur_direction)
        new_direction = random.choice(directions)

    # we look if there is dirt in the adjacent cells
    for dir in DIRECTIONS:
        if percepts['dirt-sensor-{0}'.format(dir)] == True:
            # there is dirt, that's a better direction to move to
            new_direction = dir
            break

    # if we changed direction, we add an action to change it
    if new_direction != cur_direction:
        actions.append('change-direction-{0}'.format(new_direction))

    return actions


"""
Model-based reflex agent: 
- The agent keeps track of the walls it crashed against by using a GridMap
- Based on the current wheels direction, if the next tile is a wall,
the agent will change direction
- In all the other situations, the agent will behave like the simple-reflex agent
"""

w_env = int(DISPLAY_WIDTH/ TILE_SIZE)
h_env = int(DISPLAY_HEIGHT/TILE_SIZE)
environment_map = GridMap(w_env, h_env, None)


def future_state(model, cur_location, direction):
    offset = {
        'north': (0, -1),
        'south': (0, 1),
        'west': (-1, 0),
        'east': (1, 0)
    }
    cur_x, cur_y = cur_location
    new_x, new_y = (cur_x + offset[direction][0], cur_y + offset[direction][1])

    try:
        value = model.get_item_value(new_x, new_y)
        new_location = (new_x, new_y)
    except:
        # if here it means that the next location will be out of bounds
        # so that's a wall
        value = 'W'
        new_location = None

    return value, new_location


def model_based_reflex_behaviour(percepts, actuators):
    # we can start from the actions determined by the simple reflex agent
    actions = simple_reflex_behaviour(percepts, actuators)

    # if there was a collision, I need to update the model
    cur_direction = actuators['wheels-direction']
    agent_location = percepts['location-sensor']
    if percepts['bumper-sensor-{0}'.format(cur_direction)] == True:
        _, future_location = future_state(environment_map, agent_location, cur_direction)
        if future_location is not None:
            environment_map.set_item_value(future_location[0], future_location[1], 'W')

    # we check if among the actions
    # selected by the simple-reflex behaviour
    # there is one to change direction
    new_direction = cur_direction
    for action in actions:
        if action.startswith('change-direction'):
            # this means that we hit a wall or there is dirt around the agent
            # we save this as future direction
            tokens = action.split('-')
            new_direction = tokens[2]
            # and remove it from the actions
            actions.remove(action)

    # we need to check the adjacent cells for walls
    valid_directions = []
    for direction in DIRECTIONS:
        future_state_value, _ = future_state(environment_map, agent_location, direction)
        if future_state_value != 'W':
            valid_directions.append(direction)

    # now we can check if the new direction is among the
    # valid directions with no walls
    # if not, we need to change it with a valid one
    if new_direction not in valid_directions:
        new_direction = random.choice(valid_directions)

    # if we changed direction, we add an action to change it
    if new_direction != cur_direction:
        actions.append('change-direction-{0}'.format(new_direction))

    return actions


"""
Goal-based agent:
- The agent keeps track of previously explored tiles by using a GridMap
- Based on the current wheels direction, if the next tile was already explored,
the agent will change direction towards an unexplored tile (if any, otherwise 
it will proceed in the same direction)
- In all the other situations, the agent will behave like the model-based reflex agent
- The agent will stop cleaning once the environment is fully explored
"""


def goal_based_behaviour(percepts, actuators):
    # we can start from the actions determined by the model-based reflex agent
    # doing this will also update the map with walls
    actions = model_based_reflex_behaviour(percepts, actuators)

    # we can also update the current cell as visited
    agent_location = percepts['location-sensor']
    environment_map.set_item_value(agent_location[0], agent_location[1], 'X')

    # we check if among the actions
    # selected by the model-based reflex behaviour
    # there is one to change direction
    cur_direction = actuators['wheels-direction']
    new_direction = cur_direction
    for action in actions:
        if action.startswith('change-direction'):
            # this means that we hit a wall,
            # there is dirt around the agent,
            # or there is a wall towards us
            # we save this as future direction
            tokens = action.split('-')
            new_direction = tokens[2]
            # and remove it from the actions
            actions.remove(action)

    # we determine the valid directions
    # with previously unexplored tiles
    valid_directions = []
    for direction in DIRECTIONS:
        future_state_value, _ = future_state(environment_map, agent_location, direction)
        if future_state_value is None:
            valid_directions.append(direction)

    # we check if the new direction is among the valid ones
    # and that valid_directions is not empty
    # if not, we change it
    if len(valid_directions) > 0 and new_direction not in valid_directions:
        # we change direction
        new_direction = random.choice(valid_directions)

    # if we changed direction, we add an action to change it
    if new_direction != cur_direction:
        actions.append('change-direction-{0}'.format(new_direction))

    # if we visited all the environment, we shut down the power
    if len(environment_map.find_value(None)) == 0:
        actions.append('stop-cleaning')

    return actions


"""
Utility-based agent:
The agent also stores information about dirt on the adjacent cells detected by the dirt sensors.
The agent then chooses the next direction via a utility function.
This utility function takes a direction as input, and implement the following steps:
- The agent examines its internal model of the world and retrieves a list of cell values 
in the specified direction.
- It filters out any cells that are obstructed by a wall, considering only the unobstructed cells.
- If there is dirt in the considered direction, the utility is returned as a high value such as 999
otherwise
- The agent calculates the minimum distance (min_dist) from an unexplored cell in this 
filtered list. If there are no unexplored cells, min_dist is set to a high value such as 999.
- The utility value is determined as -1 multiplied by min_dist, 
reflecting the notion that the agent values smaller distances to unexplored cells.
"""


def utility_function(model, cur_location, direction):
    x, y = cur_location
    # take the cells in the given direction
    if direction == 'north':
        cells = model.get_column(x)
        cells = np.flip(cells[0:y])
    elif direction == 'south':
        cells = model.get_column(x)
        cells = cells[y + 1:]
    elif direction == 'west':
        cells = model.get_row(y)
        cells = np.flip(cells[0:x])
    elif direction == 'east':
        cells = model.get_row(y)
        cells = cells[x + 1:]
    else:
        cells = []

    # remove the cells obstructed by a wall
    filtered_cells = []
    for cell in cells:
        if cell != 'W':
            filtered_cells.append(cell)
        else:
            # wall
            break

    # check if there is dirt in that direction
    for cell in filtered_cells:
        if cell == 'D':
            # there is dirt, return high utility
            return 999

    # compute the min distance from unexplored cells
    min_dist = 999
    i = 0
    for cell in filtered_cells:
        if cell is None:
            min_dist = i
            break
        i += 1

    # return the utility as -1*min_dist
    return -1 * min_dist


def utility_based_behaviour(percepts, actuators):
    # we can start from the actions determined by the goal-based agent
    # doing this will also update the map with walls and explored cells
    actions = goal_based_behaviour(percepts, actuators)

    # we update the environment map with information about the dirt on adjacent cells
    agent_location = percepts['location-sensor']
    for direction in DIRECTIONS:
        if percepts['dirt-sensor-{0}'.format(direction)] == True:
            _, new_location = future_state(environment_map, agent_location, direction)
            environment_map.set_item_value(new_location[0], new_location[1], 'D')

    # we remove from the actions any change of direction
    # as we determine the best direction based on the utility function
    for action in actions:
        if action.startswith('change-direction'):
            actions.remove(action)

    # we determine the best direction
    cur_direction = actuators['wheels-direction']
    max_value = None
    best_dir = None
    for direction in DIRECTIONS:
        cur_utility = utility_function(environment_map, agent_location, direction)
        if max_value is None or cur_utility > max_value:
            max_value = cur_utility
            best_dir = direction

    # if we changed direction, we add an action to change it
    if best_dir != cur_direction:
        actions.append('change-direction-{0}'.format(best_dir))

    return actions
