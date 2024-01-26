import random
from game import Player, Move, Game
from mcts import MonteCarloTreeSearchNode, PN_MCTS_Node
from board import Board


# Random player
class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


# MCTS standard version
class MonteCarloPlayer(Player):
    def __init__(self, player_id, duration, c_param) -> None:
            self.duration = duration
            self.c_param = c_param
            self.player_id = player_id
            
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        root = MonteCarloTreeSearchNode(Board(game.get_board()), player_id=self.player_id, d=0, 
                                        root_player=self.player_id,id=0,duration=self.duration, 
                                        c_param=self.c_param)
        selected_node = root.best_action()
        from_pos, move = selected_node.get_action()
        return from_pos, move

   
# PNS-MCTS variant
class MonteCarloPNSPlayer(Player):
    def __init__(self, player_id, duration = 1, c_param = 0.1, pn_param = 0.1) -> None:
        self.duration = duration
        self.c_param = c_param
        self.pn_param = pn_param     # hyperparameter used to give a weight to the PN part of the equation
                                     # used in the selection step of the tree_policy
        self.player_id = player_id

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        root = PN_MCTS_Node(Board(game.get_board()), player_id = self.player_id, 
                                        root_player = self.player_id, duration = self.duration, 
                                        c_param = self.c_param, pn_param = self.pn_param)
        selected_node = root.best_action()
        from_pos, move = selected_node.get_action()
        return from_pos, move