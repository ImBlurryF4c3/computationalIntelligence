import numpy as np
from random import choice
from nim_agent import *
from nim import play_game
from matplotlib import pyplot as plt

AGENTS = [gabriele, pure_random, optimal]
NUM_ROWS = 5

# La fitness che voglio implementare è la seguente:
# Faccio giocare il mio agent N volte con vari player che sfruttano diverse strategie
# la mia fitness conta il numero di vittorie sulle N giocate e torna la percentuale di vittorie
def fitness(my_agent: NimAgent, n_games):
    wins = 0
    next_one = n_games/len(AGENTS)
    for game in range(n_games):
        index = int(game // next_one)
        oppo_strategy = AGENTS[index]
        strategy = choice([(my_agent.choose_move, oppo_strategy), (oppo_strategy, my_agent.choose_move)])
        winner = play_game(strategy, NUM_ROWS)
        if winner == strategy.index(my_agent.choose_move):
            wins+=1
    victory_perc = wins/n_games * 100
    return victory_perc


# λ is the size of the population/the number of offspring
# μ is the number of parents selected each generation
# σ is the variance of the gaussian used to update/mutate the parameters
# + strategy: the parents are DETERMINISTICALLY selected from the (multi-)set of
# BOTH the parents and offspring
def es_mu_plus_lambda(λ, μ, rules, generations, n_games):
    # 1) Initialize parent population (μ random individuals)
    # my single individual will be characterized by a set of weights (one for each rule my agent uses)
    parents = np.random.random((λ, len(rules)+1))

    best_fitness = None
    best_weights = None
    history = list()
    for gen in range(generations):
        # 2) Generate λ offspring that will form the offspring population
        # - Select (randomly) μ parents from the parent population
        indexes = np.random.randint(0, μ, size=(λ,)) # crea un array di λ numeri interi casuali nell’intervallo [0, μ).
        offspring = np.array([deepcopy(parents[i]) for i in indexes])

        # - Mutate all σ (variance of the gaussian) and replace negative values with a small number
        offspring[:, -1] = np.random.normal(loc = offspring[:, -1], scale=0.2)
        offspring[offspring[:, -1] < 1e-5, -1] = 1e-5
        # - Mutate all the offspring with the mutated σ
        offspring[:, 0:-1] = np.random.normal(
        loc=offspring[:, 0:-1], scale=offspring[:, -1].reshape(-1, 1)
        )

        # plus-strategy: the new parent population is selected from both the offspring and parent population
        population = np.vstack([parents, offspring])
        # 3) Select new parent population
        # - evaluate the fitness of the whole population
        scores = list()
        # for each set of weights
        for i in population:
            my_agent = NimAgent(i[0:-1], rules) # I create the agent associated to this specific set of weight
            # I let him play N times against various opponents
            scores.append(fitness(my_agent, n_games))
        
        # - ranking on the results of the fitness function
        ranking_ind = np.argsort(scores)
        population = population[ranking_ind]
        # - select top μ individuals as parents for the next generation
        parents = np.copy(population[-μ:])

        # for the plot
        best_of_gen = np.array(scores)[ranking_ind][-1]
        if best_fitness is None or best_fitness < best_of_gen:
            best_fitness = best_of_gen
            best_weights = parents[-1][0:-1]
            history.append((gen, best_fitness))
            print(f'GENERATION {gen+1}: best_fitness ---> {best_fitness}')
    
    print(f'The best set of weights for my agent is the following one: {best_weights}')

    # Plot per verificare ci siano effettivi miglioramenti
    history = np.array(history)
    plt.plot(history[:, 0], history[:, 1], marker=".")
    plt.show()

def test(weights, oppo_strategy, ngames, rules):
    wins = 0
    my_agent = NimAgent(weights, rules)
    for _ in range(ngames):
      strategy = choice([(my_agent.choose_move, oppo_strategy), (oppo_strategy, my_agent.choose_move)])
      winner = play_game(strategy, 5)
      if winner == strategy.index(my_agent.choose_move):
          wins+=1
    perc = wins/ngames * 100
    print(perc)
