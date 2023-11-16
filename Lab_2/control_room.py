from es_strategy import *
import numpy as np

MU = 5
LAMBDA = 20


# Poi da togliere
N_RULES = 3

if __name__ == "__main__":
    
    # initializes a random population of λ individuals
    population = np.random.random((LAMBDA, N_RULES))
    print(population.size)
    σ = 0.001
    

    for gen in range(1_000):
        population, σ = es_mu_plus_lambda(LAMBDA, MU, σ, population)
        print(population.size)
        print(f'Step {gen}')