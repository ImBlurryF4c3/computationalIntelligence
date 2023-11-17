from nim import Nimply,Nim
import random
import numpy as np

from copy import deepcopy
import logging
from pprint import pformat



#---------------------------- OPPONENT AGENTS --------------------------------------------------------------------

# RANDOM AGENT
def pure_random(state: Nim) -> Nimply:
    """A completely random move"""
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)


# GABRIELE AGENT
def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))


# OPTIMAL AGENT
def nim_sum(state: Nim) -> int:
    tmp = np.array([tuple(int(x) for x in f"{c:032b}") for c in state.rows])
    xor = tmp.sum(axis=0) % 2
    return int("".join(str(_) for _ in xor), base=2)


def analize(raw: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = dict()
    for ply in (Nimply(r, o) for r, c in enumerate(raw.rows) for o in range(1, c + 1)):
        tmp = deepcopy(raw)
        tmp.nimming(ply)
        cooked["possible_moves"][ply] = nim_sum(tmp)
    return cooked


def optimal(state: Nim) -> Nimply:
    analysis = analize(state)
    logging.debug(f"analysis:\n{pformat(analysis)}")
    spicy_moves = [ply for ply, ns in analysis["possible_moves"].items() if ns != 0]
    if not spicy_moves:
        spicy_moves = list(analysis["possible_moves"].keys())
    ply = random.choice(spicy_moves)
    return ply

#-------------------------------------------------------------------------------------------------------------



#---------------------------------------------- OUR AGENT ----------------------------------------------------


# This class represents our agent, the one that uses the weights that are updated through an ES-startegy
class NimAgent:
    rules = list()
    weights = list()

    def __init__(self, weights, rules):
        self.weights = weights
        self.rules = rules
    
    def choose_move(self, state:Nim) -> Nimply:
        # More efficient working on ndarray
        np_weights = np.array(self.weights)
        indexes = np.argsort(np_weights)
        priority_queue = np.array(self.rules)[indexes][::-1]

        move = None
        for rule in priority_queue:
            ply = rule(state)
            if ply != None:
                move = ply
                break 
        
        return move
    

""" POSSIBLE IMPLEMENTATION --- GIVING A PROB TO THE WEIGHTS AND CHOOSING RANDOMLY (ROULETE SELECTION FOR THE MOVE)
# If I have negative weights I turn off the corresponding rule (AKA prob = 0.0)
        np_weights[np_weights[::] < 0] = 0

        
        
        # I want to choose a move randomly
        # taking in consideration that an higher value of the weight means an higher probability of being picked

        # It's like a roulette wheel selection
        tot_sum = np.sum(np_weights)
        # form weights to probabilities
        probs = list()
        cumulative_probs = list()
        for w in np_weights:
            probs.append(w/tot_sum)
            # compting the comulative probability associated to each weight
            cumulative_probs.append(np.sum(probs))
        
        
        # Now i select a random move: I use a random number r that will be used to select the corresponding rule
        # if the rule is applicable i will use the corresponding move
        move = None
        iterations = 0
        while move is None:
            iterations += 1
            r = random.random() # tra 0.0 e 1.0
            index = None
            for i,p in enumerate(cumulative_probs):
                if r <= p:
                    index = i
                    break
            ply = self.rules[index](state)
            if ply != None:
                move = ply
            # It could happen that a certain set of rules is not applicable in the actual state of the game
            # so this loop could last forever, I use a counter to break the loop after a certain number of iterations
            if iterations == 1_000:
                iterations = 0
                print(f'probs: {probs}')
                print(cumulative_probs)
                print('Sto selezionando una mossa applicabile ma casuale\n')
                break
"""