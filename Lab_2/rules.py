from nim import Nim,Nimply

# Regole basate sul numero di oggetti rimasti nel gioco

#take the first row you find with even number of remaining matches
def rule_is_even(state: Nim):
    for index_r,row in enumerate(state.rows):
        if row % 2 == 0 and row != 0:
            return Nimply(index_r,1)
    return None

#take the first row you find with odd number of remaining matches
def rule_is_odd(state: Nim):
    for index_r,row in enumerate(state.rows):
        if row % 2 != 0 and row != 0:
            return Nimply(index_r,1)

    return None 

def rule_is_odd_2(state: Nim):
    for index_r,row in enumerate(state.rows):
        if row % 2 != 0 and row > 1 :
            return Nimply(index_r,2)