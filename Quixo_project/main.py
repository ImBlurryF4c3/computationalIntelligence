import random
from game import Game, Player
from players import RandomPlayer, MonteCarloPlayer
import numpy as np
import tqdm


if __name__ == '__main__':
    players = np.empty(2, dtype=Player)
    ns = 10
    c = 0.1
    wins = 0
    matches = 0
    tot = 100

    my_player_id = random.randint(0,1)
    players[my_player_id] = MonteCarloPlayer(my_player_id, ns, 0.5)
    players[1-my_player_id] = RandomPlayer()
    g = Game()
    g.play(players[0], players[1])