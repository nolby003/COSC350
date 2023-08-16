from une_ai.tictactoe import TicTacToeGame
from une_ai.tictactoe import TicTacToePlayer

from tictactoe_game_environment import TicTacToeGameEnvironment
from tictactoe_ttable import TicTacToeTTable

from agent_programs import agent_program_random
from agent_programs import agent_program_minimax, agent_program_minimax_alpha_beta, agent_program_optimised_minimax
from agent_programs import agent_program_mcts

if __name__ == '__main__':
    # Creating the transposition table
    tt = TicTacToeTTable(instance_id='6879eb26-1ba1-11ee-8577-9e02763478a3')
    print("Initialised a Transposition table with instance id {0}".format(tt.get_instance_id()))

    wrapped_minimax_tt = lambda perc, act: agent_program_optimised_minimax(perc, act, tt, max_depth=4)

    # Creating the two players
    # To change their behaviour, change the second parameter
    # of the constructor with the desired agent program function
    player_X = TicTacToePlayer('X', agent_program_minimax_alpha_beta)
    player_O = TicTacToePlayer('O', lambda perc, act: agent_program_minimax_alpha_beta(perc, act, 10))

    # DO NOT EDIT THE FOLLOWING INSTRUCTIONS!
    environment = TicTacToeGameEnvironment()
    environment.add_player(player_X)
    environment.add_player(player_O)

    game = TicTacToeGame(player_X, player_O, environment)

