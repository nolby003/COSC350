"""
You can import modules if you need
NOTE:
your code must function properly without 
requiring the installation of any additional 
dependencies beyond those already included in 
the Python package une_ai
"""

# import ...
import pygame.math
import math
import random
import numpy as np

from queue import Queue, LifoQueue, PriorityQueue

from dataclasses import dataclass, field
from typing import Any

from snake_agent import SnakeAgent

from une_ai.models import Agent
from une_ai.models import GraphNode, GridMap
from une_ai.assignments.snake_game import DISPLAY_HEIGHT, DISPLAY_WIDTH, TILE_SIZE

# Here you can create additional functions
# you may need to use in the agent program function

DIRECTIONS = SnakeAgent.SNAKE_DIRECTIONS
EAT_STATUS = SnakeAgent.SNAKE_EAT_STATUS

h_env = DISPLAY_HEIGHT
w_env = DISPLAY_WIDTH
environment_map = GridMap(w_env, h_env, None)


def euclieanDistance(x, y):
    return pow(pow(x[0] - y[0], 2) + pow(x[1] - y[1], 2), .5)


"""
TODO:
You must implement this function with the
agent program for your snake agent.
Please, make sure that the code and implementation 
of your agent program reflects the requirements in
the assignment. Deviating from the requirements
may result to score a 0 mark in the
agent program criterion.

Please, do not change the parameters of this function.
"""


def snake_agent_program(percepts, actuators):

    global environment_map

    actions = []

    # get copy of eat status from snake_agent.py
    eat_status = EAT_STATUS.copy()

    # ------------
    # get snake current travelling x and y coords
    # ------------
    dx = percepts['body-sensor'][0][0]
    dy = percepts['body-sensor'][0][1]
    agent_location = (dx, dy)
    agent_body = percepts['body-sensor'][0]

    # fx = percepts['food-sensor'][0]
    # fy = percepts['food-sensor'][1]
    # fz = percepts['food-sensor'][2]
    food_location = (percepts['food-sensor'][0], percepts['food-sensor'][1], percepts['food-sensor'][2])
    # print('Food Locations: {0}'.format(food_location))

    print(percepts['obstacles-sensor'])
    # ox = percepts['obstacles-sensor'][0]
    # oy = percepts['obstacles-sensor'][0]
    # obstacle_location = (percepts['obstacles-sensor'][0], percepts['obstacles-sensor'][1])
    # print('Obstacle Locations: {0}'.format(obstacle_location))
    # obslist = []
    # obslist.append([percepts['obstacles-sensor'][0], percepts['obstacles-sensor'][1]])
    # print('Obstacle Locations: {0}'.format(obslist))
    # environment_map.set_item_value(agent_location[0], agent_location[1], 'X')
    # environment_map.set_item_value(food_location[0], food_location[1], 'F')

    # ------------
    # direction of snake agent
    # validation: cannot go opposing direction as is illegal
    # ------------
    directions = DIRECTIONS.copy()
    cur_direction = actuators['head']
    if cur_direction == 'up' or cur_direction == 'down':
        directions.remove('up')
        directions.remove('down')
    elif cur_direction == 'left' or cur_direction == 'right':
        directions.remove('left')
        directions.remove('right')
    # ------------

    # print to terminal direction snake is travelling
    print('Head direction: {0}'.format(cur_direction))

    # print to terminal coordinates snake is currently at (x, y)
    print("body: X:", dx, " Y:", dy)

    # ------------
    # setting collision detection coords: boundary walls
    # ------------
    # wallX = 64
    # wallY = 48
    wallX = int(w_env / 10)
    wallY = int(h_env / 10)
    # print(w_env/10, h_env/10)
    # --------------

    # --------------
    # Collision Detection - Food
    # --------------
    foodxlist = []
    foodylist = []
    for fx0, fy0, fz0 in percepts['food-sensor']:
        foodxlist.append(fx0)
        foodylist.append(fy0)

    if cur_direction == 'up':
        if agent_location[0] in foodxlist and agent_location[1] - 1 in foodylist:
            actions.append('open-mouth')
            print('Ate food')
        else:
            actions.append('close-mouth')
    if cur_direction == 'down':
        if agent_location[0] in foodxlist and agent_location[1] + 1 in foodylist:
            actions.append('open-mouth')
            print('Ate food')
        else:
            actions.append('close-mouth')
    if cur_direction == 'left':
        if agent_location[0] - 1 in foodxlist and agent_location[1] in foodylist:
            actions.append('open-mouth')
            print('Ate food')
        else:
            actions.append('close-mouth')
    if cur_direction == 'right':
        if agent_location[0] + 1 in foodxlist and agent_location[1] in foodylist:
            actions.append('open-mouth')
            print('Ate food')
        else:
            actions.append('close-mouth')
    # --------------

    # --------------
    # Collision Detection - Walls (Obstacles)
    # --------------
    for ox, oy in percepts['obstacles-sensor']:

        if cur_direction == 'up':
            if agent_location[0] == ox and agent_location[1] - 1 == oy:
                new_direction = 'left'
                actions.append('change-direction-{0}'.format(new_direction))

        if cur_direction == 'left':
            if agent_location[0] - 1 == ox and agent_location[1] == oy:
                new_direction = 'up'
                actions.append('change-direction-{0}'.format(new_direction))

        if cur_direction == 'down':
            if agent_location[0] == ox and agent_location[1] + 1 == oy:
                new_direction = 'left'
                actions.append('change-direction-{0}'.format(new_direction))

        if cur_direction == 'right':
            if agent_location[0] + 1 == ox and agent_location[1] == oy:
                new_direction = 'down'
                actions.append('change-direction-{0}'.format(new_direction))
    # --------------

    # --------------
    # define bounds
    # --------------
    top_left_corner = (0, 0)
    top_right_corner = (wallX - 1, 0)
    top_bound = (range(0, wallX - 1), 0)
    right_bound = (wallX - 1, range(0, wallY - 1))
    bottom_left_corner = (0, wallY - 1)
    bottom_right_corner = (wallX - 1, wallY - 1)
    bottom_bound = (range(1, wallX - 1), wallY - 1)
    left_bound = (0, range(0, wallY - 1))
    # --------------

    # --------------
    # Collision Detection - Game Bounds
    # --------------
    if agent_location[0] == top_left_corner[0] and agent_location[1] == top_left_corner[1]:
        print('top left corner')
        if cur_direction == 'left':
            new_direction = 'down'
            actions.append('change-direction-{0}'.format(new_direction))
        if cur_direction == 'up':
            new_direction = 'right'
            actions.append('change-direction-{0}'.format(new_direction))

    if agent_location[0] == top_right_corner[0] and agent_location[1] == top_right_corner[1]:
        print('top right corner')
        if cur_direction == 'right':
            new_direction = 'down'
            actions.append('change-direction-{0}'.format(new_direction))
        if cur_direction == 'up':
            new_direction = 'left'
            actions.append('change-direction-{0}'.format(new_direction))

    if agent_location[0] in top_bound[0] and agent_location[1] == top_bound[1]:
        print('top wall')
        new_direction = 'left'
        print('Turning {0}'.format(new_direction))
        actions.append('change-direction-{0}'.format(new_direction))

    if agent_location[0] == right_bound[0] and agent_location[1] in right_bound[1]:
        print('right wall')
        if cur_direction == 'right':
            new_direction = 'down'
            print('Turning {0}'.format(new_direction))
            actions.append('change-direction-{0}'.format(new_direction))
        if cur_direction == 'up':
            new_direction = 'left'
            print('Turning {0}'.format(new_direction))
            actions.append('change-direction-{0}'.format(new_direction))
        if cur_direction == 'down':
            new_direction = 'left'
            print('Turning {0}'.format(new_direction))
            actions.append('change-direction-{0}'.format(new_direction))

    if agent_location[0] == bottom_left_corner[0] and agent_location[1] == bottom_left_corner[1]:
        print('bottom left corner')
        if cur_direction == 'left':
            new_direction = 'up'
            actions.append('change-direction-{0}'.format(new_direction))
        if cur_direction == 'down':
            new_direction = 'right'
            actions.append('change-direction-{0}'.format(new_direction))

    if agent_location[0] == bottom_right_corner[0] and agent_location[1] == bottom_right_corner[1]:
        print('bottom right corner')
        if cur_direction == 'right':
            new_direction = 'up'
            actions.append('change-direction-{0}'.format(new_direction))
        if cur_direction == 'down':
            new_direction = 'left'
            actions.append('change-direction-{0}'.format(new_direction))

    if agent_location[0] in bottom_bound[0] and agent_location[1] == bottom_bound[1]:
        print('bottom wall')
        if cur_direction == 'left':
            new_direction = 'up'
            print('Turning {0}'.format(new_direction))
            actions.append('change-direction-{0}'.format(new_direction))
        if cur_direction == 'down':
            new_direction = 'left'
            print('Turning {0}'.format(new_direction))
            actions.append('change-direction-{0}'.format(new_direction))

    if agent_location[0] == left_bound[0] and agent_location[1] in left_bound[1]:
        print('left wall')
        if cur_direction == 'left':
            new_direction = 'down'
            actions.append('change-direction-{0}'.format(new_direction))
        if cur_direction == 'down':
            new_direction = 'right'
            actions.append('change-direction-{0}'.format(new_direction))
        if cur_direction == 'up':
            new_direction = 'right'
            actions.append('change-direction-{0}'.format(new_direction))
    # --------------

    # --------------
    # Collision Detection - Snake body
    # --------------
    for body in percepts['body-sensor']:
        if agent_location[0] == body[0] and agent_location[1] == body[1]:
            new_direction = random.choice(directions)
            actions.append('change-direction-{0}'.format(new_direction))
    # --------------

    # --------------
    # AI Search for food
    # --------------
    # find the shortest path from snake head to food and head for food item
    distX = []
    distY = []
    # run through all food locations, get fx and fy
    # find fx smallest to dx based on distance between agent and food
    # set fx to the smallest distance
    # travel by fx
    # when reach fx, travel by fy

    # works but there is collision to either obstacles or itself
    global setfx, setfy
    for x, y, z in food_location:
        distX.append(agent_location[0] - x)
        # print('DistX: {0}'.format(distX))

        distY.append(agent_location[1] - y)
        # print('DistY: {0}'.format(distY))

        minfx = min(distX)
        # print('SetFX: {0}'.format(minfx))

        x_ind = distX.index(minfx)
        # print('DistX Index chosen: {0}'.format(x_ind))

        setfx = foodxlist[x_ind]
        setfy = foodylist[x_ind]
        # print('SetFX: {0}'.format(setfx))
        # print('SetFY: {0}'.format(setfy))

    if cur_direction == 'up':
        if agent_location[1] == setfy:
            print(f'I See food!', (setfx, setfy))
        if setfx < agent_location[0]:
            new_direction = 'left'
            actions.append('change-direction-{0}'.format(new_direction))
        elif setfx > agent_location[0]:
            new_direction = 'right'
            actions.append('change-direction-{0}'.format(new_direction))

    if cur_direction == 'down':
        if agent_location[0] == setfx:
            print(f'I See food!', (setfx, setfy))
        if setfx < agent_location[0]:
            new_direction = 'left'
            actions.append('change-direction-{0}'.format(new_direction))
        elif setfx > agent_location[1]:
            new_direction = 'right'
            actions.append('change-direction-{0}'.format(new_direction))

    if cur_direction == 'left':
        if agent_location[0] == setfx:
            print(f'I See food!', (setfx, setfy))
        if setfy < agent_location[1]:
            new_direction = 'up'
            actions.append('change-direction-{0}'.format(new_direction))
        elif setfy > agent_location[1]:
            new_direction = 'down'
            actions.append('change-direction-{0}'.format(new_direction))

    if cur_direction == 'right':
        if agent_location[0] == setfx:
            print(f'I See food!', (setfx, setfy))
        if setfy < agent_location[1]:
            new_direction = 'up'
            actions.append('change-direction-{0}'.format(new_direction))
        elif setfy > agent_location[1]:
            new_direction = 'down'
            actions.append('change-direction-{0}'.format(new_direction))
    # --------------

    return actions
