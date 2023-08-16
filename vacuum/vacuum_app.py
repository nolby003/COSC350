from une_ai.vacuum import VacuumGame
from vacuum_agent import VacuumAgent
from agent_programs import test_behaviour, simple_reflex_behaviour, model_based_reflex_behaviour, goal_based_behaviour, utility_based_behaviour

if __name__ == "__main__":
    # creating the vacuum agent
    # To test the different agent programs, change the function passed 
    # as parameter when instantiating the class VacuumAgent
    agent = VacuumAgent(model_based_reflex_behaviour)

    # running the game with the instantiated agent
    # DO NOT EDIT THIS INSTRUCTION!
    game = VacuumGame(agent)