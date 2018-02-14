import random
from functools import reduce
from operator import add

from deap import creator, base, tools, algorithms
import utils

MIN_GEN_VAL = -1
MAX_GEN_VAL = 1

GEN_PER_INDIVIDUAL = 100
POPULATION = 300
GENERATIONS_PER_EPOCH = 25
MAX_GENERATIONS = 10000
EPSILON = 1e-5


class Algorithm(object):
    """
        Representation of a genetic algorithm to find function minimums
    """

    def __init__(self, function):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        self.toolbox.register("gene", random.uniform, MIN_GEN_VAL, MAX_GEN_VAL)
        self.toolbox.register("individual", tools.initRepeat,
                              creator.Individual, self.toolbox.gene,
                              n=GEN_PER_INDIVIDUAL)
        self.toolbox.register("population", tools.initRepeat, list,
                              self.toolbox.individual)

        self.function = function
        self.toolbox.register("evaluate", utils.min_value(function))
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def calculate(self, x1 = None, x2 = None):
        population = self.toolbox.population(n=POPULATION)
        last_min = None
        gens = 0
        while True:
            for gen in range(GENERATIONS_PER_EPOCH):
                offspring = algorithms.varAnd(population, self.toolbox, cxpb=0.5,
                                          mutpb=0.1)
                # Filter out records out of range
                if x1:
                    offspring = [ind for ind in offspring if reduce(add, ind, 0) >= x1]
                if x2:
                    offspring = [ind for ind in offspring if reduce(add, ind, 0) <= x2]

                fits = self.toolbox.map(self.toolbox.evaluate, offspring)
                for fit, ind in zip(fits, offspring):
                    ind.fitness.values = fit
                population = self.toolbox.select(offspring, k=len(population))
            
            best = tools.selBest(population, k=1)
            
            current_min = reduce(add, best[0], 0)
            if last_min:
                if abs(current_min - last_min) < EPSILON:
                    return current_min
            last_min = current_min
            
            gens += GENERATIONS_PER_EPOCH
            if gens > MAX_GENERATIONS:
                return


    def check_if_range_has_minimum(self, previous_derivative, derivative):
        # if the X axis is passed for this range the previous derivative
        # should have a different sign
        found_extremum = previous_derivative * derivative <= 0
        return found_extremum and previous_derivative <= 0

    def check_all_ranges(self, ranges):
        results = []
        for r in ranges:
            x1 = r[0]
            x2 = r[1]
            self.toolbox.register("evaluate",
                                  utils.min_value(self.function))
            result = self.calculate(x1, x2)
            results.append(result)
        return results

    def find_local_minimums(self, min_val=-100, max_val=100, grid=0.1):
        previous_derivative = None
        range_limits = []
        for i in utils.drange(min_val, max_val, grid):
            x1 = i - grid/2
            x2 = i + grid/2
            # we calculate the derivative in order to check whether
            # the selected range includes a local extremum or not
            derivative = utils.calculate_derivative(self.function, x1, x2)
            if previous_derivative:
                if self.check_if_range_has_minimum(previous_derivative,
                                                   derivative):
                    range_limits.append((x1 - grid, x2))
            previous_derivative = derivative
        return self.check_all_ranges(range_limits)
