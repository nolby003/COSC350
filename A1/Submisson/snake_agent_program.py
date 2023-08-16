"""
You can import modules if you need
NOTE:
your code must function properly without 
requiring the installation of any additional 
dependencies beyond those already included in 
the Python package une_ai
"""
import random

# import ...
from une_ai.models import Agent
from snake_agent import SnakeAgent

# Here you can create additional functions
# you may need to use in the agent program function

DIRECTIONS = SnakeAgent.SNAKE_DIRECTIONS
EAT_STATUS = SnakeAgent.SNAKE_EAT_STATUS

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
    global ox, oy
    actions = []

    # get copy of eat status from snake_agent.py
    eat_status = EAT_STATUS.copy()

    # ------------
    # get snake current travelling x and y coords
    # ------------
    dx = percepts['body-sensor'][0][0]
    dy = percepts['body-sensor'][0][1]
    # ------------

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
    # print('Head direction: {0}'.format(cur_direction))

    # print to terminal coordinates snake is currently at (x, y)
    # print("\nbody: X:", dx, " Y:", dy)

    # ------------
    # setting collision detection coords: boundary walls
    # ------------
    wallX = 64
    wallY = 48

    boundX = wallX - 1
    boundY = wallY - 1
    if dx < 0 or dx > 64 or dy < 0 or dy < 48:
        bounds = 1
    else:
        bounds = 0
    # print('Bounds: ', bounds)
    # ------------

    # when agent travelling up
    if actuators['head'] == 'up':

        # ------------
        # Collision detection: boundary walls
        #
        # when boundary wall approaches, move snake in a different direction (that does not intercept another wall)
        #
        # Top left corner wall
        # ------------
        if dx == 0 and dy == 0:
            print('Hit Top left corner wall')
            print('Heading right')
            actions.append('change-direction-right')
        # ------------

        # ------------
        # Collision detection: boundary walls
        #
        # when boundary wall approaches, move snake in a different direction (that does not intercept another wall)
        #
        # Top wall
        # ------------
        if dx in range(1, boundX) and dy == 0:
            directions = DIRECTIONS.copy()
            print('Hit Top wall')
            directions.remove('up')
            directions.remove('down')
            for ox, oy in percepts['obstacles-sensor']:
                if dy - 1 == oy:
                    print("Obstacle to our left, changing direction to right")
                    new_direction = 'left'
                elif dy + 1 == oy:
                    print("Obstacle to our right, changing direction to left")
                    new_direction = 'right'
            if len(directions) != 1:
                new_direction = random.choice(directions)
            else:
                new_direction = directions[0]
            print('Heading {0}'.format(new_direction))
            actions.append('change-direction-{0}'.format(new_direction))
        # ------------

        # ------------
        # Collision detection: boundary walls
        #
        # when boundary wall approaches, move snake in a different direction (that does not intercept another wall)
        #
        # Top right corner wall
        # ------------
        if dx == boundX and dy == 0:
            print('Hit Top right corner wall')
            print('Heading left')
            actions.append('change-direction-left')
        # ------------

        # ------------
        # Collision detection: obstacles
        #
        # when obstacle approaches, move snake in a different direction (that does not intercept another obstacle)
        #
        # ox = obstacle x, oy = obstacle y
        # ------------
        for ox, oy in percepts['obstacles-sensor']:
            if dy - 1 == oy and dx == ox:
                print('Hit an obstacle, checking for a safe path...')
                # check obstacle coord just before hitting it
                # and check not on it
                # and check if a wall exists
                if dx - 1 != ox or dx != ox:
                    print('Nothing on left, heading left')
                    actions.append('change-direction-left')
                elif dx + 1 != ox:
                    print('Nothing on right, heading right')
                    actions.append('change-direction-right')
        # ------------

        # ------------
        # Collision detection, hunting and eating food
        #
        # when travelling:
        #   find food on other coordinate
        #   change direction toward food coordinate
        #   open mouth just before food coordinate
        #   eat food on coordinate
        #   close mouth after coordinate
        #   continue travelling
        #
        # fx = food x coord, fy = food y coord, s = points value
        #
        # tried to build logic to check food y coord for an intercepting obstacle but failed
        # wanted to see if I could see food in L.O.S rather than behind obstacles
        # this also causes the agent to turn into obstacles toward food when on a boundary wall to cause Game over
        # ------------
        for fx, fy, s in percepts['food-sensor']:
            if dy == fy:
                print(f'I See food!', (fx, fy))
                if fx < dx:
                    actions.append('change-direction-left')
                    print('Heading left')
                elif fx > dx:
                    actions.append('change-direction-right')
                    print('Heading right')
            if dy + 1 == fy and dx == fx:
                actions.append('open-mouth')
                # print(f'Mouth open-r', (dx+1, dy))
            else:
                actions.append('close-mouth')
                # print(f'Mouth closed-r', (dx, dy))
            if dx == fx and dy == fy:
                print(f'Ate food-u', (dx, dy), (fx, fy))
        # ------------

    # when agent travelling down
    if actuators['head'] == 'down':

        # ------------
        # Collision detection: boundary walls
        #
        # when boundary wall approaches, move snake in a different direction (that does not intercept another wall)
        #
        # Bottom left corner wall
        # ------------
        if dx == 0 and dy == boundY:
            print('Hit Bottom left corner wall')
            print('Heading right')
            actions.append('change-direction-right')
        # ------------

        # ------------
        # Collision detection: boundary walls
        #
        # when boundary wall approaches, move snake in a different direction (that does not intercept another wall)
        #
        # Bottom wall
        # ------------
        if dx in range(1, boundX) and dy == boundY:
            directions = DIRECTIONS.copy()
            print('Hit Bottom wall')
            directions.remove('up')
            directions.remove('down')
            for ox, oy in percepts['obstacles-sensor']:
                if dy - 1 == oy and dx == ox:
                    print("Obstacle to our left, changing direction to right")
                    directions.remove('left')
                elif dy + 1 == oy and dx == ox:
                    print("Obstacle to our right, changing direction to left")
                    directions.remove('right')
            if len(directions) != 1:
                new_direction = random.choice(directions)
            else:
                new_direction = directions[0]
            print('Heading {0}'.format(new_direction))
            actions.append('change-direction-{0}'.format(new_direction))
        # ------------

        # ------------
        # Collision detection: boundary walls
        #
        # when boundary wall approaches, move snake in a different direction (that does not intercept another wall)
        #
        # Bottom right corner wall
        # ------------
        if dx == boundX and dy == boundY:
            print('Hit Bottom right corner wall')
            print('Heading left')
            actions.append('change-direction-left')
        # ------------

        # ------------
        # Collision detection: obstacles
        #
        # when obstacle approaches, move snake in a different direction (that does not intercept another obstacle)
        #
        # ox = obstacle x, oy = obstacle y
        # ------------
        for ox, oy in percepts['obstacles-sensor']:
            if dy + 1 == oy and dx == ox:
                print('Hit an obstacle, checking for a safe path...')
                if dx - 1 != ox and dx - 1 != 0 and dx != 0:
                    print('Nothing on left, heading left')
                    actions.append('change-direction-left')
                else:
                    print('Nothing on right, heading right')
                    actions.append('change-direction-right')
        # ------------

        # ------------
        # Collision detection, hunting and eating food
        #
        # when travelling:
        #   find food on other coordinate
        #   change direction toward food coordinate
        #   open mouth just before food coordinate
        #   eat food on coordinate
        #   close mouth after coordinate
        #   continue travelling
        #
        # fx = food x coord, fy = food y coord, s = points value
        #
        # tried to build logic to check food y coord for an intercepting obstacle but failed
        # wanted to see if I could see food in L.O.S rather than behind obstacles
        # this also causes the agent to turn into obstacles toward food when on a boundary wall to cause Game over
        # ------------
        for fx, fy, s in percepts['food-sensor']:
            if dy == fy:
                print(f'I See food!', (fx, fy))
                if fx < dx:
                    actions.append('change-direction-left')
                    print('Heading left')
                elif fx > dx:
                    actions.append('change-direction-right')
                    print('Heading right')
            if dy + 1 == fy and dx == fx:
                actions.append('open-mouth')
                # print(f'Mouth open-r', (dx+1, dy))
            else:
                actions.append('close-mouth')
                # print(f'Mouth closed-r', (dx, dy))
            if dx == fx and dy == fy:
                print(f'Ate food-d', (dx, dy), (fx, fy))
        # ------------

    # when agent travelling left
    if actuators['head'] == 'left':

        # ------------
        # Collision detection: boundary walls
        #
        # when boundary wall approaches, move snake in a different direction (that does not intercept another wall)
        #
        # Top left corner wall
        # ------------
        if dx == 0 and dy == 0:
            print('Hit Top left corner wall')
            print('Heading left')
            actions.append('change-direction-down')
        # ------------

        # ------------
        # Collision detection: boundary walls
        #
        # when boundary wall approaches, move snake in a different direction (that does not intercept another wall)
        #
        # Left wall
        # ------------
        if dx == 0 and dy in range(1, boundY):
            directions = DIRECTIONS.copy()
            print('Hit Left wall')
            directions.remove('left')
            directions.remove('right')
            new_direction = random.choice(directions)
            print('Heading {0}'.format(new_direction))
            actions.append('change-direction-{0}'.format(new_direction))
        # ------------

        # ------------
        # Collision detection: boundary walls
        #
        # when boundary wall approaches, move snake in a different direction (that does not intercept another wall)
        #
        # Bottom left corner wall
        # ------------
        if dx == 0 and dy == boundY:
            print('Hit Bottom left corner wall')
            print('Heading up')
            actions.append('change-direction-up')
        # ------------

        # ------------
        # Collision detection: obstacles
        #
        # when obstacle approaches, move snake in a different direction (that does not intercept another obstacle)
        #
        # ox = obstacle x, oy = obstacle y
        # ------------
        for ox, oy in percepts['obstacles-sensor']:
            if dx - 1 == ox and dy == oy:
                print('Hit an obstacle, checking for a safe path...')
                if dy - 1 != oy and dx != 0 and dy != 0:  # need to fix heading left and going up when should go down
                    print('Nothing above, heading up')
                    actions.append('change-direction-up')
                elif dy + 1 != oy and dx != 64 and dy != 64:
                    print('Nothing below, heading down')
                    actions.append('change-direction-down')
        # ------------

        # ------------
        # Collision detection, hunting and eating food
        #
        # when travelling:
        #   find food on other coordinate
        #   change direction toward food coordinate
        #   open mouth just before food coordinate
        #   eat food on coordinate
        #   close mouth after coordinate
        #   continue travelling
        #
        # fx = food x coord, fy = food y coord, s = points value
        # ------------
        for fx, fy, s in percepts['food-sensor']:
            if dx == fx:
                print(f'I See food!', (fx, fy))
                if fy < dy:
                    actions.append('change-direction-up')
                    print('Heading up')
                elif fy > dy:
                    actions.append('change-direction-down')
                    print('Heading down')
            if dx + 1 == fx and dy == fy:
                actions.append('open-mouth')
                # print(f'Mouth open-l', (dx-1, dy))
            else:
                actions.append('close-mouth')
                # print(f'Mouth closed-l', (dx, dy))
            if dx == fx and dy == fy:
                print(f'Ate food-l', (dx, dy), (fx, fy))
        # ------------

    # when agent travelling right
    if actuators['head'] == 'right':

        # ------------
        # Collision detection: boundary walls
        #
        # when boundary wall approaches, move snake in a different direction (that does not intercept another wall)
        #
        # Top right corner wall
        # ------------
        if dx == boundX and dy == 0:
            print('Hit Top right corner wall')
            print('Heading down')
            actions.append('change-direction-down')
        # ------------

        # ------------
        # Collision detection: boundary walls
        #
        # when boundary wall approaches, move snake in a different direction (that does not intercept another wall)
        #
        # Right wall
        # ------------
        if dx == boundX and dy in range(1, boundY):
            directions = DIRECTIONS.copy()
            print('Hit Right wall')
            directions.remove('left')
            directions.remove('right')
            new_direction = random.choice(directions)
            print('Heading {0}'.format(new_direction))
            actions.append('change-direction-{0}'.format(new_direction))
        # ------------

        # ------------
        # Collision detection: boundary walls
        #
        # when boundary wall approaches, move snake in a different direction (that does not intercept another wall)
        #
        # Bottom right corner wall
        # ------------
        if dx == boundX and dy == boundY:
            print('Hit Bottom right corner wall')
            print('Heading up')
            actions.append('change-direction-up')
        # ------------

        # ------------
        # Collision detection: obstacles
        #
        # when obstacle approaches, move snake in a different direction (that does not intercept another obstacle)
        #
        # ox = obstacle x, oy = obstacle y
        # ------------
        for ox, oy in percepts['obstacles-sensor']:
            if dx + 1 == ox and dy == oy:
                print('Hit an obstacle, checking for a safe path...')
                if dy - 1 != oy and dy != 0:
                    print('Nothing above, heading up')
                    actions.append('change-direction-up')
                elif dy != oy and dy != 48:
                    print('Nothing below, heading down')
                    actions.append('change-direction-down')
        # ------------

        # ------------
        # Collision detection, hunting and eating food
        #
        # when travelling:
        #   find food on other coordinate
        #   change direction toward food coordinate
        #   open mouth just before food coordinate
        #   eat food on coordinate
        #   close mouth after coordinate
        #   continue travelling
        #
        # fx = food x coord, fy = food y coord, s = points value
        # ------------
        for fx, fy, s in percepts['food-sensor']:
            if dx == fx:
                print(f'I See food!', (fx, fy))
                if fy < dy:
                    actions.append('change-direction-up')
                    print('Heading up')
                elif fy > dy:
                    actions.append('change-direction-down')
                    print('Heading down')
            if dx + 1 == fx and dy == fy:
                actions.append('open-mouth')
                # print(f'Mouth open-r', (dx+1, dy))
            else:
                actions.append('close-mouth')
                # print(f'Mouth closed-r', (dx, dy))
            if dx == fx and dy == fy:
                print(f'Ate food-r', (dx, dy), (fx, fy))
        # ------------

    # -------------
    # previous code for collision detection - walls
    # -------------
    # # Top left corner wall
    # if dx == 0 and dy == 0:
    #     print('Hit Top left corner wall')
    #     if actuators['head'] == 'up':
    #         print('Going right')
    #         actions.append('change-direction-right')
    #     elif actuators['head'] == 'left':
    #         print('Going left')
    #         actions.append('change-direction-down')
    #
    # # Top wall
    # #if dx in range(1, boundX-1) and dy == 0:
    # if topwall == 1:
    #     directions = DIRECTIONS.copy()
    #     print('Hit Top wall')
    #     if actuators['head'] == 'up':
    #         directions.remove('up')
    #         directions.remove('down')
    #         new_direction = random.choice(directions)
    #         print('Going {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #
    # # Top right corner wall
    # if dx == boundX and dy == 0:
    #     print('Hit Top right corner wall')
    #     if actuators['head'] == 'up':
    #         print('Going left')
    #         actions.append('change-direction-left')
    #     elif actuators['head'] == 'right':
    #         print('Going down')
    #         actions.append('change-direction-down')
    #
    # # Left wall
    # #if dx == 1 and dy in range(1, boundY-1):
    # if leftwall == 1:
    #     directions = DIRECTIONS.copy()
    #     print('Hit Left wall')
    #     if actuators['head'] == 'left':
    #         directions.remove('left')
    #         directions.remove('right')
    #         new_direction = random.choice(directions)
    #         print('Going {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #
    # # Bottom left corner wall
    # if dx == 0 and dy == boundY:
    #     print('Hit Bottom left corner wall')
    #     if actuators['head'] == 'down':
    #         print('Going right')
    #         actions.append('change-direction-right')
    #     elif actuators['head'] == 'left':
    #         print('Going up')
    #         actions.append('change-direction-up')
    #
    # # Bottom wall
    # #if dx in range(1, boundX-1) and dy == boundY:
    # if bottomwall == 1:
    #     directions = DIRECTIONS.copy()
    #     print('Hit Bottom wall')
    #     if actuators['head'] == 'down':
    #         directions.remove('up')
    #         directions.remove('down')
    #         new_direction = random.choice(directions)
    #         print('Going {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #
    # # Bottom right corner wall
    # if dx == boundX and dy == boundY:
    #     print('Hit Bottom right corner wall')
    #     if actuators['head'] == 'down':
    #         print('Going left')
    #         actions.append('change-direction-left')
    #     elif actuators['head'] == 'right':
    #         print('Going up')
    #         actions.append('change-direction-up')
    #
    # # Right wall
    # #if dx == boundX and dy == 1:
    # if rightwall == 1:
    #     directions = DIRECTIONS.copy()
    #     print('Hit Right wall')
    #     if actuators['head'] == 'right':
    #         directions.remove('left')
    #         directions.remove('right')
    #         new_direction = random.choice(directions)
    #         print('Going {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    # --------------
    # --------------

    # --------------
    # --------------
    # old code below for for collision detection - walls
    # --------------
    # if actuators['head'] == 'up':
    #     directions = DIRECTIONS.copy()
    #     if dx in range(0, boundX) and dy == 0:  # top boundary - must go left or right
    #         directions.remove('up')
    #         directions.remove('down')
    #         new_direction = random.choice(directions)
    #         print('\nWall! At {0} Turn {1}'.(x,y), format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #         print('\nMoving {0}'.format(new_direction))
    #     if dx == 1 and dy == 0:  # top left corner - must go right
    #         new_direction = 'right'
    #         print('\nWall! Turn {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #         print('\nMoving {0}'.format(new_direction))
    #     if dx == boundX and dy == 0:  # top right corner - must go left
    #         new_direction = 'left'
    #         print('\nWall! Turn {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #         print('\nMoving {0}'.format(new_direction))
    #
    # if actuators['head'] == 'down':
    #     directions = DIRECTIONS.copy()
    #     if dx in range(0, boundX) and dy == boundY:  # bottom boundary - must go left or right
    #         directions.remove('up')
    #         directions.remove('down')
    #         new_direction = random.choice(directions)
    #         print('\nWall! Turn {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #         print('\nMoving {0}'.format(new_direction))
    #     if dx == 0 and dy == boundY:  # bottom left corner - must go right
    #         new_direction = 'right'
    #         print('\nWall! Turn {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #         print('\nMoving {0}'.format(new_direction))
    #     if dx == boundX and dy == boundY:  # bottom right corner - must go left
    #         new_direction = 'left'
    #         print('\nWall! Turn {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #         print('\nMoving {0}'.format(new_direction))
    #
    # if actuators['head'] == 'left':
    #     directions = DIRECTIONS.copy()
    #     if dx == 1 and dy in range(0, boundY):  # left boundary - must go up or down
    #         directions.remove('left')
    #         directions.remove('right')
    #         new_direction = random.choice(directions)
    #         print('\nWall! Turn {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #         print('\nMoving {0}'.format(new_direction))
    #     if dx <= 1 and dy <= 1:  # top left corner - must go down
    #         new_direction = 'down'
    #         print('\nWall! Turn {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #         print('\nMoving {0}'.format(new_direction))
    #     if dx <= 1 and dy == boundY:  # bottom left corner - must go up
    #         new_direction = 'up'
    #         print('\nWall! Turn {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #         print('\nMoving {0}'.format(new_direction))
    #
    # if actuators['head'] == 'right':
    #     directions = DIRECTIONS.copy()
    #     if dx == boundX and dy in range(0, boundY):  # right boundary - must go up or down
    #         directions.remove('left')
    #         directions.remove('right')
    #         new_direction = random.choice(directions)
    #         print('\nWall! Turn {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #         print('\nMoving {0}'.format(new_direction))
    #     if dx == boundX and dy == 0:  # top right corner - must go down
    #         new_direction = 'down'
    #         print('\nWall! Turn {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #         print('\nMoving {0}'.format(new_direction))
    #     if dx == boundX and dy == boundY:  # bottom right corner - must go up
    #         new_direction = 'up'
    #         print('\nWall! Turn {0}'.format(new_direction))
    #         actions.append('change-direction-{0}'.format(new_direction))
    #         print('\nMoving {0}'.format(new_direction))
    # --------------
    # --------------

    # -------------
    # previous code for collision detection - obstacles
    # -------------
    # ------------
    # check if obstacles found
    # move snake in a different direction
    # ------------
    # for x, y in percepts['obstacles-sensor']:
    #
    #     if actuators['head'] == 'up':
    #         # print(x, y)
    #         if dy - 1 == y and dx == x:
    #             print('Hit an obstacle, checking for a safe path...')
    #             if dx - 1 != x:
    #                 print('Nothing on left, going left')
    #                 actions.append('change-direction-left')
    #             elif dx + 1 != x:
    #                 print('Nothing on right, going right')
    #                 actions.append('change-direction-right')
    #
    #     if actuators['head'] == 'down':
    #         # print(x, y)
    #         if dy + 1 == y and dx == x:
    #             print('Hit an obstacle, checking for a safe path...')
    #             if dx - 1 != x:
    #                 print('Nothing on left, going left')
    #                 actions.append('change-direction-left')
    #             elif dx + 1 != x:
    #                 print('Nothing on right, going right')
    #                 actions.append('change-direction-right')
    #
    #     if actuators['head'] == 'left':
    #         # print(x, y)
    #         if dx - 1 == x and dy == y:
    #             print('Hit an obstacle, checking for a safe path...')
    #             if dy - 1 != y and dx != 0:
    #                 print('Nothing above, going up')
    #                 actions.append('change-direction-up')
    #             elif dy + 1 != y and dx != 64:
    #                 print('Nothing below, going down')
    #                 actions.append('change-direction-down')
    #
    #     if actuators['head'] == 'right':
    #         # print(x, y)
    #         if dx + 1 == x and dy == y:
    #             print('Hit an obstacle, checking for a safe path...')
    #             if dy - 1 != y and dy != 0:
    #                 print('Nothing above, going up')
    #                 actions.append('change-direction-up')
    #             elif dy != y and dy != 48:
    #                 print('Nothing below, going down')
    #                 actions.append('change-direction-down')
    # --------------
    # --------------

    # --------------
    # --------------
    # old code below for collision detection - obstacles
    # --------------
    # if actuators['head'] == 'down':
    #     print(x, y)
    #     if dx - 1 != x:
    #         print('Nothing on left, going left')
    #         actions.append('change-direction-left')
    #     elif dx + 1 != x and dx != boundX:
    #         print('Nothing on right, going right')
    #         actions.append('change-direction-right')
    #
    # if actuators['head'] == 'left':
    #     print(x, y)
    #     if dy - 1 != y and dy != 0:
    #         print('Nothing above, going up')
    #         actions.append('change-direction-up')
    #     elif dy + 1 != y and dy != 48:
    #         print('Nothing below, going down')
    #         actions.append('change-direction-down')
    #
    # if actuators['head'] == 'right':
    #     print(x, y)
    #     if dy - 1 != y and dy != 0:
    #         print('Nothing above, going up')
    #         actions.append('change-direction-up')
    #     elif dy + 1 != y and dy != 48:
    #         print('Nothing below, going down')
    #         actions.append('change-direction-down')

    # directions = DIRECTIONS.copy()
    # # snake travelling up
    # # hits obstacle
    # # checks around if another obstacle is present
    # # chooses direction where it won't hit another obstacle
    # if actuators['head'] == 'up':
    #     directions.remove('up')
    #     directions.remove('down')
    #     if dy - 1 == y:  # condition we are about to hit an obstacle (WORKS)
    #         print(x, y)
    #         # check surroundings for other obstacles
    #         # is there no obstacle on our left? Go left.
    #         if dx - 1 != x:
    #             new_direction = 'left'
    #             actions.append('change-direction-{0}'.format(new_direction))
    #             print('\nObstacle! Turn {0}'.format(new_direction))
    #             print('\nMoving {0}'.format(new_direction))
    #         # is there no obstacle on our right? Go right.
    #         elif dx + 1 != x:
    #             new_direction = 'right'
    #             actions.append('change-direction-{0}'.format(new_direction))
    #             print('\nObstacle! Turn {0}'.format(new_direction))
    #             print('\nMoving {0}'.format(new_direction))
    #
    # # snake travelling down
    # # hits obstacle
    # # changes direction
    # if actuators['head'] == 'down':
    #     directions.remove('down')
    #     directions.remove('up')
    #     if dy + 1 == y:  # condition we are about to hit an obstacle
    #         print(x, y)
    #         # check surroundings for other obstacles
    #         # is there no obstacle on our left? Go left.
    #         if dx - 1 != x and dx - 1 not in range(0, 1):
    #             new_direction = 'left'
    #             actions.append('change-direction-{0}'.format(new_direction))
    #             print('\nObstacle! Turn {0}'.format(new_direction))
    #             print('\nMoving {0}'.format(new_direction))
    #         # is there no obstacle on our right? Go right.
    #         elif dx + 1 != x:
    #             new_direction = 'right'
    #             actions.append('change-direction-{0}'.format(new_direction))
    #             print('\nObstacle! Turn {0}'.format(new_direction))
    #             print('\nMoving {0}'.format(new_direction))
    # # # snake travelling left
    # # # hits obstacle
    # # # changes direction
    # if actuators['head'] == 'left':
    #     directions.remove('left')
    #     directions.remove('right')
    #     # scenario where we hit an obstacle facing up,
    #     turned left and an adjacent obstacle was detected based on y
    #     # so removed y as part of the condition and focused on x
    #     if dx - 1 == x and dy == y:  # condition we are about to hit an obstacle
    #         print(x, y)
    #         # check surroundings for other obstacles
    #         # is there no obstacle above us? Go up.
    #         if dy - 1 != y:
    #             new_direction = 'up'
    #             actions.append('change-direction-{0}'.format(new_direction))
    #             print('\nObstacle! Turn {0}'.format(new_direction))
    #             print('\nMoving {0}'.format(new_direction))
    #         # is there no obstacle below us? Go down.
    #         elif dy + 1 != y:
    #             new_direction = 'down'
    #             actions.append('change-direction-{0}'.format(new_direction))
    #             print('\nObstacle! Turn {0}'.format(new_direction))
    #             print('\nMoving {0}'.format(new_direction))
    # # # snake travelling right
    # # # hits obstacle
    # # # changes direction
    # if actuators['head'] == 'right':
    #     directions.remove('left')
    #     directions.remove('right')
    #     if dx + 1 == x:  # condition we are about to hit an obstacle
    #         print(x, y)
    #         # check surroundings for other obstacles
    #         # is there no obstacle above us? Go up.
    #         if dy - 1 != y:
    #             new_direction = 'up'
    #             actions.append('change-direction-{0}'.format(new_direction))
    #             print('\nObstacle! Turn {0}'.format(new_direction))
    #             print('\nMoving {0}'.format(new_direction))
    #         # is there no obstacle below us? Go down.
    #         elif dy + 1 != y:
    #             new_direction = 'down'
    #             actions.append('change-direction-{0}'.format(new_direction))
    #             print('\nObstacle! Turn {0}'.format(new_direction))
    #             print('\nMoving {0}'.format(new_direction))
    # --------------
    # --------------

    # --------------
    # previous code for collision detection - food
    # --------------
    # ------------
    # hunt for food
    # check if snake found food
    # open snake's mouth
    # eat food
    # close mouth
    # ------------
    # for x, y, z in percepts['food-sensor']:
    #
    #     if actuators['head'] == 'up':
    #         # checking on Y to find food that matches snake's Y
    #         # there was an instance that the snake would travel to the first in sight
    #         # if another intercepted, it would change paths
    #         # at times if two food squares were near, the snake would loop turns infinitely
    #         if dy == y:
    #             print('\nI See food!')
    #             print(x, y)
    #             if x < dx:
    #                 actions.append('change-direction-left')
    #             else:
    #                 actions.append('change-direction-right')
    #         if dx == x and dy - 1 == y:
    #             actions.append('open-mouth')
    #         if dx == x and dy == y:
    #             actions.append('close-mouth')
    #
    #     if actuators['head'] == 'left':
    #         # checking on X to find food that matches snake's X
    #         if dx == x:
    #             print('\nI See food!')
    #             print(x, y)
    #             if y < dy:
    #                 actions.append('change-direction-up')
    #             elif y > dy:
    #                 actions.append('change-direction-down')
    #         if dx - 1 == x and dy == y:
    #             actions.append('open-mouth')
    #             # if dx == x and dy == y:
    #             actions.append('close-mouth')
    #
    #     if actuators['head'] == 'right':
    #         # checking on X to find food that matches snake's X
    #         if dx == x:
    #             print('\nI See food!')
    #             print(x, y)
    #             if y > dy:
    #                 actions.append('change-direction-down')
    #             else:
    #                 actions.append('change-direction-up')
    #         if dx + 1 == x and dy == y:
    #             actions.append('open-mouth')
    #             # if dx == x and dy == y:
    #             actions.append('close-mouth')
    #
    #     if actuators['head'] == 'down':
    #         # checking on Y to find food that matches snake's Y
    #         if dy == y:
    #             print('\nI See food!')
    #             print(x, y)
    #             if x < dx:
    #                 actions.append('change-direction-left')
    #             elif x > dx:
    #                 actions.append('change-direction-right')
    #         if dx == x and dy + 1 == y:
    #             actions.append('open-mouth')
    #             # if dx == x and dy == y:
    #             actions.append('close-mouth')
    # --------------
    # --------------

    return actions
