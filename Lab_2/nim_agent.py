from nim import Nimply,Nim
import random
import numpy as np
from rules import *


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


RULES = [rule_is_even,
         rule_is_odd,
         rule_is_odd_2]


# This class represents our agent, the one that uses the weights that are updated through an ES-startegy
class NimAgent:
    rules = RULES
    weights = list()
    fitness = None

    def __init__(self, weights):
        self.weights = weights

    def setFitness(self,value):
        self.fitness = value

    def getFitness(self):
        if self.fitness == None:
            print("Error, you're acceding a None fitness value")
        return self.fitness
    
    def choose_move(self, state:Nim) -> Nimply:
        # More efficient working on ndarray
        np_weights = np.array(self.weights)

        # @Blurryface
        # Implemento la roulette wheel selection
        tot_sum = np.sum(np_weights)
        # passso da peso a probabilità
        probs = list()
        cumulative_probs = list()
        for w in self.weights:
            probs.append(w/tot_sum)
            # calcolo la probabilità comulativa associata ad ogni peso
            cumulative_probs.append(np.sum(probs))
        # Adesso devo selezionare un peso casualmente e utilizzare il suo indice per scegliere la regola corrispondente
        # Ovviamente circolo fino a quando la regola selezionata è applicabile
        move = None
        while move is None:
            r = random.random() # tra 0.0 e 1.0
            index = None
            for i,p in enumerate(cumulative_probs):
                if r <= p:
                    index = i
                    break
            ply = self.rules[index](state)
            if ply != None:
                move = ply

        if move == None:
            move = pure_random(state)
            
        return move
    
    """
    def analize(raw: Nim) -> list:
        possibles = list()
        # The following for loop creates all the possible_moves
        # It verifies the number of remaining objects for each row and creates a Nimply(row_id,match_id) object
        # for r, c in enumerate(raw.rows) ----> r is the index of the row, c contains the number of objects in it
        # for o in range(1, c + 1) ---> o starts from 1 to c (numbers of object) + 1
        for ply in (Nimply(r, o) for r, c in enumerate(raw.rows) for o in range(1, c + 1)):     
           possibles.append(ply)
        return possibles
    """



