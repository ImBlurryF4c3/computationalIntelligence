from nim import Nim,Nimply
import numpy as np
from random import choice

B_PERC = 30
A_PERC = 80


# A set of rules that I can use for my agent
# Every ruke returns a specific move if applicable otherwise it returns None

# If the percentage of sticks in a row is <= to B_PERC
# I take all the remaining objects of the row
def rule_take_all_if_below(state: Nim):
    for row,n_objects in enumerate(state.rows):
        if n_objects == 0:
            continue
        total_objects = row*2 + 1
        percentage = n_objects/total_objects * 100
        if percentage <= B_PERC:
            return Nimply(row, n_objects)
    return None

# If the percentage of sticks in a row is >= to A_PERC
# I take half of the sticks in the row (rounded down -> 5/2 = 2 NOT 3)
def rule_take_half_if_above(state: Nim):
    for row,n_objects in enumerate(state.rows):
        total_objects = row*2 + 1
        percentage = n_objects/total_objects * 100
        if percentage >= A_PERC:
            to_take = n_objects//2
            if to_take == 0:
                to_take = 1
            return Nimply(row, to_take)
    return None

# If the row has an even number of remaining objects, I take 1
def rule_take_if_even(state: Nim):
    for row,n_objects in enumerate(state.rows):
        if n_objects == 0:
            continue
        if n_objects % 2 == 0:
            return Nimply(row, 1)
    return None

# If the row has an odd number of remaining objects, I take 1
def rule_take_if_odd(state: Nim):
    for row,n_objects in enumerate(state.rows):
        if n_objects == 0:
            continue
        if n_objects % 2 != 0:
            return Nimply(row, 1)
    return None

# I select a random row where I can take 2 sticks from
def rule_take_2(state: Nim):
    mask = np.array(state.rows) >= 2
    is_possible = any(mask)
    if is_possible:
        row = choice([i for i,_ in enumerate(state.rows) if mask[i]])
        return Nimply(row, 2)
    return None

# I take all the remaining objects from the row with the most sticks
# I don't do this move only if there is one remaining row with sticks
def rule_eliminate_row(state: Nim):
    rows_with_objects = sum(np.array(state.rows) > 0)
    if rows_with_objects == 1:
        return None
    mask = np.array(state.rows) > 0
    row = choice([i for i,_ in enumerate(state.rows) if mask[i]])
    return Nimply(row, state.rows[row])