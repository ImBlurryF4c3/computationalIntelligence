import logging
from collections import namedtuple


Nimply = namedtuple("Nimply", "row, num_objects")

# Class object for the game
class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects

# strategy: tupla che contiene due funzioni che corrispondono alle strategie implementate 
# dai player 0 e 1 rispettivamente -> Scelgo la strategia che utilizzeranno i due player
# num_rows: int che indica il numero di righe del mio NIM game 
def play_game(strategy, num_rows):
    #logging.getLogger().setLevel(logging.INFO)

    nim = Nim(num_rows)
    logging.info(f"init : {nim}")
    player = 0

    while nim:
        # ritorna una delle mosse applicabili nello stato attuale di 'nim'
        ply = strategy[player](nim)
        #logging.info(f"ply: player {player} plays {ply}")

        # applica la mossa
        nim.nimming(ply)
        #logging.info(f"status: {nim}")

        # Now the other player plays
        player = 1 - player
    logging.info(f"status: Player {player} won!")

    return player