# gameplay pseudo
# two teams: Gold Diggers (Miners) and Saboteurs
# miners goal is to build tunnels to reach the gold
# saboteurs goal is to prevent it and reach the gold themselves
# card decks (Path/goal, Path/action, nugget, dwarf)
# shuffle identity cards (dwarf cards)
# if there are 3 players, 3 cards are dealt, and 1 left to the side (non player)
# start card placed 7 cards length away from the 3 goal cards, goal cards are shuffled, one will be a gold card and the other two are coal
# board dimensions ix 8x5
# path cards and action cards are shuffled into a single deck
# x cards are handed to each player
# remaining cards as a deck
# shuffle gold nugget cards and placed them as a deck
# player is chosen at random and then in order of that initial shuffle
# each player's turn is playing a card: either placing a path card, giving out an action card or pass and discard a card into the discard pile
# then player draws a card from the remaining deck
# when remaining deck is gone, player need to use up all their cards: path, action(mend/sabotage) or discard
# path cards must be placed again the last path card and must attempt to go in the direction toward the goal cards
# path cards cannot be played cross-wise (match up symmetrically)
# a mend action card can only mend a sabotage card of the same type
# the dynamite card is used to remove a path card from the board, excluding start and goal cards
# the map card allows a player to look at one of the goal cards
# when a player uses a path card that connects directly to the goal card, the goal card can be revealed
# if there is a clear path from the start card to the gold card, the Miners win
# if the card is a stone/coal, the game continues
# when the miners do win, the player that was able to turn the gold card, gets to choose a nugget card and pass the rest to each of the remaining miners
# the player with the most gold nuggets wins
# if two miners have the same amunt of nuggets, it is a tie
# if a miner has a sabotage card that is a broken axe, they do not receive nugget cards, even if the miners won, does not apply if the saboteurs win


from saboteur_game import SaboteurGame
from saboteur_environment import SaboteurEnvironment
from saboteur_player import SaboteurPlayer
from agent_programs import miner_behaviour, saboteur_behaviour

PYGAME_DETECT_AVX2 = 1

if __name__ == '__main__':
    nplayers = 3
    agent_miner = SaboteurPlayer('Miner', miner_behaviour, nplayers)
    agent_saboteur = SaboteurPlayer('Saboteur', saboteur_behaviour, nplayers)

    environment = SaboteurEnvironment()
    environment.add_player(agent_miner)
    environment.add_player(agent_saboteur)

    SaboteurGame(agent_miner, agent_saboteur, environment, nplayers)  # how many players to pass in?
