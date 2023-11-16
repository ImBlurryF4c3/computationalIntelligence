import numpy as np
from random import choice
from nim_agent import *
from nim import play_game


N = 100
AGENTS = [optimal]
NUM_ROWS = 5
best_fitness = None


# La fitness che voglio implementare è la seguente:
# Faccio giocare il mio agent N volte con vari player che sfruttano diverse strategie
# la mia fitness conta il numero di vittorie sulle N giocate e torna la percentuale di vittorie
def fitness(my_agent: NimAgent):
    wins = 0
    next_one = N/len(AGENTS)
    for game in range(N):
        index = int(game // next_one)
        oppo_strategy = AGENTS[index]
        strategy = choice([(my_agent.choose_move, oppo_strategy), (oppo_strategy, my_agent.choose_move)])
        winner = play_game(strategy, NUM_ROWS)
        if winner == strategy.index(my_agent.choose_move):
            wins+=1
    victory_perc = wins/N * 100
    return victory_perc


# La 'mutate' muta il valore dei pesi in base al valore di sigma
def mutate(weights, σ):
    # The individual is a numpy.ndarray
    new_weights = list()
    for w in weights:
        new_weights.append(np.random.normal(loc=w, scale=σ))
    return new_weights
   

# THIS FUNCTION APPLIES THE STRATEGY ONLY ONCE, IT HAS TO BE CALLED EVERY ITERATION
# λ is the size of the population
# μ is the number of parents selected each generation
# σ is the variance of the gaussian used to update/mutate the parameters
# + startegy: the offspring is generated both from parents and their children
def es_mu_plus_lambda(λ, μ, σ, population):
    global best_fitness

    # The population is characterized by a set of weights
    # n of rows equal to λ
    # each row has len(rules) weights, each one associated to a rule

    # I evaluate the fitness of the population
    scores = list()
    # for each set of weights
    for i in population:
        my_agent = NimAgent(i) # I create the agent associated to this specific set of weight
        # I let him play N times against various opponents
        scores.append(fitness(my_agent))
    # I rank the individuals
    indices = np.argsort(scores)
    population = population[indices]

    # I choose the top μ as parents for the next generation
    # REMEMBER: YOU KEEP THE PARENTS IN THE NEW POPULATION (offspring)
    parents = population[-μ:]

    best_of_gen = np.array(scores)[indices][-1]

    # Verifico se la fitness migliore è migliorata
    if best_fitness is None or best_fitness < best_of_gen:
        # Devo fare il sorting di scores
        best_fitness = best_of_gen
        print(f'UPDATED the best_fitness: {best_fitness}')

    # Self-adaptive ---> I also change σ
    σ = np.random.normal(loc=σ, scale=0.0005)
    if σ < 1e-5:
      σ = 1e-5

    n_chilldren_per_parent = int((λ-μ)/μ)
    offspring = list()
    for p in parents:
        # I keep the parent
        offspring.append(deepcopy(p))
        # each parent has n_children mutated
        for _ in range(n_chilldren_per_parent):
            offspring.append(deepcopy(mutate(p, σ)))
    offspring = np.array(offspring)
    # torna la nuova popolazione e il nuovo valore di σ
    return offspring, σ   