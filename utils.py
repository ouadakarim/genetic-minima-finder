from functools import reduce
from operator import add


# Evaluation utils - for genetic algorithm evaluation


def finite_difference(function, diff=0.01):
    def evaluation(individual):
        x = reduce(add, individual, 0)
        # Like finite differences
        # calculated manually
        rating = function(x + diff) - function(x - diff)
        return -abs(rating),
    return evaluation


def min_value(function, x1 = None, x2 = None):
    def evaluation(individual):
        x = reduce(add, individual, 0)
        val = function(x)
        # Dirty hack to exclude arguments out of range
        if x1 and x < x1:
            val = 1000000000000
        if x2 and x > x2:
            val = 1000000000000
        return -val,
    return evaluation


# Function utils - basic methods for mathematical functions


def calculate_derivative(function, x1, x2):
    derivative = (function(x1) - function(x2))/(x1-x2)
    return derivative


# Other utils

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step


