import random
from functools import reduce
from operator import add

from deap import creator, base, tools, algorithms

MIN_GEN_VAL = -1
MAX_GEN_VAL = 1


class Algorithm(object):
    """
        Representation of a genetic algorithm to find function minimums
    """
    def __init__(self, function):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        self.toolbox.register("gene", random.uniform, MIN_GEN_VAL, MAX_GEN_VAL)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.gene, n=100)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        def evaluation(individual):
            x = reduce(add, individual, 0)
            val = function(x)
            return -val,

        #TODO: Mechanizm szatkowania dla wielomianów
        self.toolbox.register("evaluate", evaluation)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def calculate(self):
        population = self.toolbox.population(n=300)
        NGEN=40
        for gen in range(NGEN):
            offspring = algorithms.varAnd(population, self.toolbox, cxpb=0.5, mutpb=0.1)
            fits = self.toolbox.map(self.toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            population = self.toolbox.select(offspring, k=len(population))
        top10 = tools.selBest(population, k=10)
        return [reduce(add, x, 0) for x in top10]

