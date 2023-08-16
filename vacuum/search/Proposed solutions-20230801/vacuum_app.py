from une_ai.vacuum import VacuumGame
from vacuum_dock_agent import VacuumDockAgent
from agent_programs import search_behaviour
from agent_programs import depth_first_search, breadth_first_search, uniform_cost_search
from agent_programs import greedy_best_first_search, A_star_search

if __name__ == "__main__":
    # To test the different agent programs implementing different search strategies
    # We need to wrap the desired search behaviour into a lambda function
    # This function will take the two expected parameters for the agent program:
    # percepts and actuators, and it will execute the search behaviour with 
    # a desired search strategies
    # To change the search strategy, change the third parameter for the search_beahviour function
    # executed by the lambda function
    agent_program = lambda percepts, actuators: search_behaviour(percepts, actuators, depth_first_search)
    
    # creating the vacuum agent with a charging dock
    agent = VacuumDockAgent(agent_program)

    # running the game with the instantiated agent
    # DO NOT EDIT THIS INSTRUCTION!
    game = VacuumGame(agent, uses_charging_dock=True)