"""
NOTE:
This file is given to you to test your code.
DO NOT EDIT THIS FILE!
"""
from une_ai.assignments import SnakeGame
from snake_agent import SnakeAgent
from snake_agent_program import snake_agent_program

# from snake_agent_program import A_star_search

PYGAME_DETECT_AVX2 = 1

#agent_program = lambda percepts, actuators: snake_agent_program(percepts, actuators, A_star_search)

if __name__ == "__main__":
    snake_agent = SnakeAgent(snake_agent_program)
    snake_game = SnakeGame(snake_agent)
