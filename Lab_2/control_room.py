from es_strategies import *
from rules import *


MU = 5
LAMBDA = 20
RULES = [rule_eliminate_row,
         rule_take_all_if_below,
         rule_take_2,
         rule_take_half_if_above,
         rule_take_if_even,
         rule_take_if_odd]

# Agenti performanti
w1 = [
    10.7011413, 
    -5.67738108, 
    -2.36507506,
    -11.90014491,
    1.84369092,
    -7.09477893
    ]
#--------------------------------------------------
w2 = [
    55.08209802,  
    14.21645598,  
    30.30528509, 
    -12.62181029,  
    37.75294224,
    0.25087804
    ]
"""
GENERATION 1: best_fitness ---> 77.0
GENERATION 2: best_fitness ---> 78.0
GENERATION 3: best_fitness ---> 83.0
GENERATION 7: best_fitness ---> 84.0
GENERATION 9: best_fitness ---> 85.0
GENERATION 10: best_fitness ---> 86.0
GENERATION 12: best_fitness ---> 88.0
GENERATION 587: best_fitness ---> 91.0
GENERATION 999: best_fitness ---> 93.0
"""


if __name__ == "__main__":
    #es_mu_plus_lambda(LAMBDA, MU, RULES, 1000, 300)
    opponent_strat = optimal
    test(w2, opponent_strat, 1000, RULES)