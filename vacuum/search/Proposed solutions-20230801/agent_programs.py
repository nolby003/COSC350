import math
import random 
import numpy as np
from queue import Queue, LifoQueue, PriorityQueue
from prioritized_item import PrioritizedItem

from une_ai.vacuum import DISPLAY_HEIGHT, DISPLAY_WIDTH, TILE_SIZE
from une_ai.models import GridMap, GraphNode
from vacuum_agent import VacuumAgent

DIRECTIONS = VacuumAgent.WHEELS_DIRECTIONS

# 1. We create a model of the environment using a GridMap
# this step is similar to Week 2 workshop when implementing
# the model based agents

w_env = int(DISPLAY_WIDTH/ TILE_SIZE)
h_env = int(DISPLAY_HEIGHT/TILE_SIZE)
environment_map = GridMap(w_env, h_env, None)

# 2. Let's model an agent program accepting
# an additional parameter search_function
# This parameter is the search function to use to find
# a path to the desired goal state
# by doing so, we can easily plug-and-play different search algorithm
# by keeping the rest of the agent program the same

# we will make use of these global variables
# to keep track of the path to the charging dock or to the
# unexplored goal tile
path_to_dock = []
path_to_unexplored = []

# creating a function to determine the future state
# given a current tile and wheels direction
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

# this agent program function is partially implemented
# and commented to help you completing its implementation
def search_behaviour(percepts, actuators, search_function):
    global path_to_dock, path_to_unexplored, environment_map # we declare these variables global

    actions = [] # we start with an empty list of actions to perform for this step

    # get agent location
    agent_location = percepts['location-sensor']

    # updating the map with the visited tile
    # set environment_map to 'X' at the present location (visited)
    environment_map.set_item_value(agent_location[0], agent_location[1], 'X')

    # updating the map with the charging dock location
    # dock_location = ...
    # set environment_map to 'C' at the charging dock location
    dock_location = percepts['charging-dock-location-sensor']
    environment_map.set_item_value(dock_location[0], dock_location[1], 'C')

    # did the agent crash against a wall?
    # retrieve the current direction of the wheels from the actuators
    cur_direction = actuators['wheels-direction']
    
    # check if the bumper sensor for that direction detected a collision or not
    # if so, get the location of the tile with the wall (the one towards the wheels' direction)
    # and update the environment_map with 'W' in that location (if not out of boundaries)
    if percepts['bumper-sensor-{0}'.format(cur_direction)] == True:
        # bumped into a wall, reset paths
        path_to_dock = []
        path_to_unexplored = []
        _, future_location = future_state(environment_map, agent_location, cur_direction)
        if future_location is not None:
            environment_map.set_item_value(future_location[0], future_location[1], 'W')
    
    # updating dirt in adjacent cells
    # for all the possible directions check if the dirt sensors detected dirt in the adjacent cells
    # if so, update the ones with dirt in the environment_map by setting their cell to 'D'
    # updating dirt in adjacent cells
    for direction in DIRECTIONS:
        if percepts['dirt-sensor-{0}'.format(direction)] == True:
            _, future_location = future_state(environment_map, agent_location, direction)
            environment_map.set_item_value(future_location[0], future_location[1], 'D')
    
    # if the power is off, we start cleaning
    if actuators['vacuum-power'] != 1:
        actions.append('start-cleaning')
    
    # if we visited and cleaned the whole environment, we stop
    # To check that, you can use the method find_value of the GridMap
    # A fully explored and cleaned environment should not have any cell to None or 'D'
    # if we visited and cleaned the whole environment, we stop
    if len(environment_map.find_value(None)) == 0 and len(environment_map.find_value('D')) == 0:
        if actuators['vacuum-power'] == 1:
            actions.append('stop-cleaning')
    
    # if there is dirt on the current tile, activate the suction mechanism
    # otherwise, if there is no dirt and the suction mechanism is on, turn it off
    # to preserve the battery
    if percepts['dirt-sensor-center']:
        actions.append('activate-suction-mechanism')
    elif actuators['suction-power'] == 1:
        actions.append('deactivate-suction-mechanism')

    # Now we can check if it is best to continue cleaning
    # or if it is best to go back to the charging dock

    # read the battery level
    # if the battery level is less than 50 (50%), then
    battery_level = percepts['battery-level']
    next_action_direction = None
    if battery_level <= 50:
        # GOING TO THE CHARGING DOCK
        # first check if there is a path to the dock (is path_to_dock empty?)
        # if there is no path to the dock, we need to find one
        if len(path_to_dock) == 0:
            # the search_function should return a goal_node (an instance of the class GraphNode)
            # given the present agent location and a goal function:
            # goal_node = search_function(agent_location, a_goal_function_for_charging_dock)
            goal_node = search_function(agent_location, is_charging_dock)
            # if the goal_node was found (not None/False), then we can generate the path to the goal
            # with the method .get_path()
            if goal_node != False:
                path_to_dock, _ = goal_node.get_path()
        
        # We can set the value of path_to_dock to the found path
        # and if now path_to_dock has at least one element, we retrieve the first item from the list
        # with the method .pop(0). That's the next action movement to perform to head towards the goal
        # so we add this action to the actions list
        if len(path_to_dock) > 0:
            next_action_direction = path_to_dock.pop(0)
    else:
        # ELSE, CONTINUE CLEANING
        # first check if there is a path to an unexplored tile (is path_to_unexplored empty?)
        # if there is no path to an unexplored tile, we need to find one
        if len(path_to_unexplored) == 0:
            # the search_function should return a goal_node (an instance of the class GraphNode)
            # given the present agent location and a goal function:
            # goal_node = search_function(agent_location, a_goal_function_to_unexplored_tiles)
            goal_node = search_function(agent_location, is_unexplored)
            # if the goal_node was found (not None/False), then we can generate the path to the goal
            # with the method .get_path()
            if goal_node != False:
                path_to_unexplored, _ = goal_node.get_path()

        # We can set the value of path_to_unexplored to the found path
        # and if now path_to_unexplored has at least one element, we retrieve the first item from the list
        # with the method .pop(0). That's the next action movement to perform to head towards the goal
        # so we add this action to the actions list
        # look for the closest unexplored tile
        if len(path_to_unexplored) > 0:
            next_action_direction = path_to_unexplored.pop(0)
    
    if next_action_direction is not None:
        actions.append(next_action_direction)
    
    return actions

# 3. Implementing the search strategies
# First, we need two ingredients:
# - A function to expand nodes from a current node
# - Goal functions to determine if a node is a desired goal state

# Expansion function
# Given a GraphNode, we generate all its successors
def expand(node):
    global environment_map
    # for every node we have four potential successors
    # based on the following possible actions:
    # 'change-direction-north', 'change-direction-south', 'change-direction-west', 'change-direction-east'
    actions = {
        'change-direction-north': (0, -1),
        'change-direction-south': (0, 1),
        'change-direction-west': (-1, 0),
        'change-direction-east': (1, 0)
    }

    # this function must add all the possible successors of node to this list
    successors = []

    # for each action, we must check if the successor is:
    # 1. Within the boundaries of the environment map
    # 2. The environment_map at the successor location was not set as wall yet ('W')
    # If the action lead to any of the two possible scenarios, the successor will not be added to the expansion 
    cur_state = node.get_state()
    for action, offset in actions.items():
        new_state = (cur_state[0] + offset[0], cur_state[1] + offset[1])
        try:
            item_in_map = environment_map.get_item_value(new_state[0], new_state[1])
        except:
            # out of bounds, it's a wall
            item_in_map = 'W'
        
        if item_in_map == 'W':
            # the agent knows that there is a wall, skip expansion for this action
            continue
        
        # to create an instance of GraphNode:
        # successor = GraphNode(successor_state, node, action, cost)
        # successor_state is the representation of the state of the successor node, e.g. the x,y coordinates
        # the second parameter is the parent node we have as input to this function
        # action is the action that generated the successor via this expansion
        # cost is the cost to be in the state of the successor node, in this scenario all nodes have the same uniform cost (i.e. 1)
        cost = 1
        successor = GraphNode(new_state, node, action, cost)

        # after creating an instance of the successor, add it to the successors list
        successors.append(successor)
    
    return successors

# Goal functions
# A goal function takes a node state as input and returns True
# if the state is a goal state and False otherwise

# For this scenario we need two goal functions:
# 1. A function telling us if the state is an unexplored or dirty tile
# 2. A function telling us if the state is the location of the charging dock
def is_unexplored(node_state):
    global environment_map
    
    # if the environment_map at the coordinates in node_state is dirty or unexplored, return True
    # else, return False
    try:
        map_item_value = environment_map.get_item_value(node_state[0], node_state[1])
    except:
        map_item_value = 'W'
    
    return True if map_item_value in ['D', None] else False

def is_charging_dock(node_state):
    global environment_map
    
    # if the environment_map at the coordinates in node_state is the location of the charging dock, return True
    # else, return False
    try:
        map_item_value = environment_map.get_item_value(node_state[0], node_state[1])
    except:
        map_item_value = 'W'
    
    return True if map_item_value == 'C' else False


# Now we can implement the functions for the search strategies
# Each search function takes two input parameters:
# 1. The coordinates where we start the search
# 2. A goal function to determine if a node is a goal state or not

# We start from the depth-first search, as you'll see it is unefficient for this scenario
def depth_first_search(start_coords, goal_function):
    # create a GraphNode for the initial state
    # with the starting coordinates as its state
    # An initial state node does not have parent node (None)
    # and action that generated it (None) and its cost can be set to 0
    initial_state = GraphNode(start_coords, None, None, 0)

    # check if the state for the initial node is a goal state
    # if so, return it
    if goal_function(initial_state.get_state()):
        return initial_state
    
    # if not, we need to create a frontier
    # for a depth-first algorithm, the frontier can be represented
    # with a LIFO queue. In Python we have the library queue 
    # including different types of queue data structures, including LifoQueue
    frontier = LifoQueue()

    # we need to input the initial state node to the frontier
    # you can use the method .put(node), with node being the node to insert into the queue
    frontier.put(initial_state)

    # we also need to set a list of all reached states
    # we also need to append the state of the initial node to the reached list
    # you can use the .append method
    reached = [initial_state.get_state()]

    # now we start a while loop until we have nodes in the frontier
    while frontier.qsize() > 0:
        # in this loop, we first get the next node from the frontier queue
        # we can do so with the method .get()
        cur_node = frontier.get()
        # then we get its successors by expanding the node with the function expand
        successors = expand(cur_node)
        # for every successor found, we check if their states are goal states with the goal_function
        for successor in successors:
            if goal_function(successor.get_state()):
                # if they are, we return the successor
                return successor
            
            # else, we check if the state of the successor is not in the reached list yet
            successor_state = successor.get_state()
            if successor_state not in reached:
                # if it is not there yet, we add the state of the successor to the reached list
                reached.append(successor_state)
                # and we insert the successor node to the frontier (using .put again)
                frontier.put(successor)
    
    # if nothing was returned so far, we return False (or None if you prefer)
    # to suggest that no solution was found for this search
    return False


# For the breadth-first search, you will see that
# the only thing changing from the depth-first implementation
# is the type of queue data structure used.
# In the depth-first search we used a LIFO queue, for the
# breadth-first search we need to use a FIFO queue.
# In Python, the queue library offer the class Queue to create
# FIFO queues
def breadth_first_search(start_coords, goal_function):
    # If you have done everything correctly for the depth-first search
    # you will simply need to re-use the depth-first search code
    # and change a single line of code to use a FIFO queue instead of
    # a LIFO one

    initial_state = GraphNode(start_coords, None, None, 0)
    if goal_function(initial_state.get_state()):
        return initial_state
    frontier = Queue() # this line changed
    frontier.put(initial_state)
    reached = [initial_state.get_state()]
    while frontier.qsize() > 0:
        cur_node = frontier.get()
        successors = expand(cur_node)
        for successor in successors:
            if goal_function(successor.get_state()):
                return successor
            successor_state = successor.get_state()
            if successor_state not in reached:
                reached.append(successor_state)
                frontier.put(successor)
        
    return False

# For the uniform cost search, the process is the same as per
# the depth-first and breadth-first searches.
# Indeed, in this scenario where the cost are the same in all nodes,
# the uniform cost search will return the same solutions as the
# breath-first search
# To implement this search strategy, you will need a priority queue
# In Python, the library queue offer the class PriorityQueue to create
# a priority queue. This queue is a bit different from the LIFO and FIFO
# queues used so far because it expects a priority value for each
# inserted item, so to sort them based on their priority (the lower the priority
# value is, the sooner the item will be retrieved from the queue).
# On the top of this script, we imported the class PrioritizedItem from the prioritized_item.py file
# This class allows you to create an object with a priority value and
# an item for the queue. PriorityQueue will use the priority value to sort the items
# To create a PrioritizedItem:
# item_for_priority_queue = PrioritizedItem(priority_value, node_to_add_to_queue)
# you can then use the .put method to insert the prioritized item you just created
# To access the node when retrieving the item from the queue:
# cur_item = my_priority_queue.get()
# cur_node = cur_item.item
def uniform_cost_search(start_coords, goal_function):
    # the implementation will be very similar to the previous
    # search strategies, just a matter of changing the queue to
    # a PriorityQueue with an appropriate cost of the path to the added node 
     
    initial_state = GraphNode(start_coords, None, None, 0)
    if goal_function(initial_state.get_state()):
        return initial_state
    # THESE LINES CHANGED
    frontier = PriorityQueue()
    _, g = initial_state.get_path()
    frontier.put(PrioritizedItem(g, initial_state))
    # --------
    reached = [initial_state.get_state()]
    while frontier.qsize() > 0:
        cur_item = frontier.get()
        cur_node = cur_item.item
        successors = expand(cur_node)
        for successor in successors:
            if goal_function(successor.get_state()):
                return successor
            successor_state = successor.get_state()
            if successor_state not in reached:
                reached.append(successor_state)
                # THESE LINES CHANGED
                _, g = successor.get_path()
                frontier.put(PrioritizedItem(g, successor))
                # -------
        
    return False

# Now we are getting to informed search strategies
# for these strategies we need an additional ingredient:
# A heuristic function to estimate the cost of the current node
# w.r.t. the expected goal

# we can consider a simple heuristic:
# - We get all the states we consider valid goal states
# - We compute the straight distances from the current node to all the identified goal states
# - Our heuristic cost will be the minimum among the estimated straight distances
# Remember that a straight distance can be computed as:
# square root of ((x1-x2)^2 + (y1-y2)^2)
# In Python the square root operation can be performed with math.sqrt
# And the power operator uses the syntax **, e.g. 2**3 will give 8

def heuristic_cost(current_node, goal_function):
    # Compute the straight distance
    # from the current_node to all goal states
    straight_distances = []
    for x in range(0, w_env):
        for y in range(0, h_env):
            if goal_function((x, y)):
                cur_dist = math.sqrt((current_node[0] - x)**2 + (current_node[1] - y)**2)
                straight_distances.append(cur_dist)
        
    # return the minimum cost among the computed distances
    return np.min(straight_distances)

# Now that we have the heuristic function, we can implement
# the greedy-best first search
def greedy_best_first_search(start_coords, goal_function):
    # It's implementation would be very similar to the
    # uniform cost search
    # However, this time the cost to add to the priority queue
    # will not be the cost of the path to reach the node
    # instead, the cost will be the cost estimated by the heuristic function

    initial_state = GraphNode(start_coords, None, None, 0)
    if goal_function(initial_state.get_state()):
        return initial_state
    frontier = PriorityQueue()
    h = heuristic_cost(initial_state.get_state(), goal_function) # This line changed
    frontier.put(PrioritizedItem(h, initial_state)) # This line changed
    reached = [initial_state.get_state()]
    while frontier.qsize() > 0:
        cur_item = frontier.get()
        cur_node = cur_item.item
        successors = expand(cur_node)
        for successor in successors:
            if goal_function(successor.get_state()):
                return successor
            successor_state = successor.get_state()
            if successor_state not in reached:
                reached.append(successor_state)
                h = heuristic_cost(successor.get_state(), goal_function) # This line changed
                frontier.put(PrioritizedItem(h, successor)) # This line changed
        
    return False

# Finally, we can implement the A* start search
# In this scenario, the costs are uniform (all 1) so 
# The A* search will return the same solutions as the greedy-best first search
# However, the implementation will be sligthly different
def A_star_search(start_coords, goal_function):
    # You can start from the implementation of the greedy-best first search
    # However, the priority value will not only be the heuristic cost
    # predicted by the heuristic function, but a sum of that cost and
    # the cost of the path to reach the node

    initial_state = GraphNode(start_coords, None, None, 0)
    if goal_function(initial_state.get_state()):
        return initial_state
    frontier = PriorityQueue()
    # THESE LINES CHANGED
    _, g = initial_state.get_path()
    h = heuristic_cost(initial_state.get_state(), goal_function)
    frontier.put(PrioritizedItem(g+h, initial_state))
    # ------
    reached = [initial_state.get_state()]
    while frontier.qsize() > 0:
        cur_item = frontier.get()
        cur_node = cur_item.item
        successors = expand(cur_node)
        for successor in successors:
            if goal_function(successor.get_state()):
                return successor
            successor_state = successor.get_state()
            if successor_state not in reached:
                reached.append(successor_state)
                # THESE LINES CHANGED
                _, g = successor.get_path()
                h = heuristic_cost(successor.get_state(), goal_function)
                frontier.put(PrioritizedItem(g+h, successor))
                # -----
        
    return False