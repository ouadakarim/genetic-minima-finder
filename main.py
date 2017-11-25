from genetics import Algorithm
from math import cos, sinh

functions = [
    lambda x: cos(x)+sinh(x)**2,  # min at 0.0
    lambda x: (x-1)*(x+4)*(x+8)*(x-6)*(x-3)*x,  # min at -6.77598
    lambda x: x**4 + 9*x**3 - 5*x**2 + 2*x + 1  # should be -7.1114
]

# TODO:
# Implement some kind of grid, so that we find global all minimums
# Maybe random or intelligent way to get correct periods

algorithm = Algorithm(functions[1])
print(algorithm.calculate())


