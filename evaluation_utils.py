from functools import reduce
from operator import add


def finite_difference(function, diff=0.01):
    def evaluation(individual):
        x = reduce(add, individual, 0)
        # Like finite differences
        # calculated manually
        rating = function(x + diff) - function(x - diff)
        return -abs(rating),
    return evaluation


def min_value(function):
    def evaluation(individual):
        x = reduce(add, individual, 0)
        val = function(x)
        return -val,
    return evaluation

