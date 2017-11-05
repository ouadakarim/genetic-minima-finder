import random
from functools import reduce
from operator import add

from deap import creator, base, tools, algorithms

MIN_GEN_VAL = -1
MAX_GEN_VAL = 1

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("genome", random.uniform, MIN_GEN_VAL, MAX_GEN_VAL)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.genome, n=100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    x = reduce(add, individual, 0)
    val = x**4 + 9*x**3 - 5*x**2 + 2*x + 1
    return -val,

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=300)

NGEN=40
for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, k=len(population))
top10 = tools.selBest(population, k=10)
print([reduce(add, x, 0) for x in top10])
