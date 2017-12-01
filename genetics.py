import random
from functools import reduce
from operator import add

from deap import creator, base, tools, algorithms
import utils

MIN_GEN_VAL = -1
MAX_GEN_VAL = 1

GEN_PER_INDIVIDUAL = 100
POPULATION = 300
GENERATIONS = 40


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

    def calculate(self):
        population = self.toolbox.population(n=POPULATION)
        for gen in range(GENERATIONS):
            offspring = algorithms.varAnd(population, self.toolbox, cxpb=0.5,
                                          mutpb=0.1)
            fits = self.toolbox.map(self.toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            population = self.toolbox.select(offspring, k=len(population))
        top10 = tools.selBest(population, k=10)
        return [reduce(add, x, 0) for x in top10]

    def check_if_range_has_minimum(self, previous_derivative, derivative):
        # if the X axis is passed for this range the previous derivative
        # should have a different sign
        found_extremum = previous_derivative * derivative <= 0
        return found_extremum and previous_derivative <= 0

    def check_all_ranges(self, ranges):
        results = []
        for i, val in enumerate(ranges):
            if i + 1 < len(ranges):
                x1 = ranges[i]
                x2 = ranges[i + 1]
                self.toolbox.register("evaluate",
                                      utils.min_value(self.function, x1, x2))
                result = self.calculate()
                results.append(result[0])
        return results

    def find_local_minimums(self, min_val=-100, max_val=100, grid=0.1):
        previous_derivative = None
        min_arr = []
        range_limits = []
        for i in utils.drange(min_val, max_val, grid):
            x1 = i + grid/2
            x2 = i - grid/2
            # we calculate the derivative in order to check whether
            # the selected range includes a local extremum or not
            derivative = utils.calculate_derivative(self.function, x1, x2)
            if previous_derivative:
                if self.check_if_range_has_minimum(previous_derivative,
                                                   derivative):
                    min_arr.append(x2)
            previous_derivative = derivative
        range_limits.append(min_val)
        for i, val in enumerate(min_arr):
            if i + 1 < len(min_arr):
                x1 = min_arr[i]
                x2 = min_arr[i + 1]
                center = (x1 + x2) / 2
                range_limits.append(center)
        range_limits.append(max_val)
        return self.check_all_ranges(range_limits)
