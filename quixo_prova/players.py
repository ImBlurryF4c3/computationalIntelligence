import random
from game import Player, Move, Game
from mcts import MonteCarloTreeSearchNode
from board import Board

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class MonteCarloPlayer(Player):
    def __init__(self, player_id, num_simulations = 100, c_param = 0.1) -> None:
            self.num_simulations = num_simulations
            self.c_param = c_param
            self.player_id = player_id
            

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        #print(f"make_move -> my player id: {self.player_id}")
        root = MonteCarloTreeSearchNode(Board(game.get_board()), player_id=self.player_id, d=0, root_player=self.player_id,id=0,num_simulations=self.num_simulations, c_param=self.c_param)
        selected_node = root.best_action()
        from_pos, move = selected_node.get_action()
        #print('In make_move del nostro player -> Il nodo selezionato è il seguente: ', selected_node)
        #print(f"In make_move del nostro player -> from_pos (col,row): {from_pos}, move: {move}")
        return from_pos, move