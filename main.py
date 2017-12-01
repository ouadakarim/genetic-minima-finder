from genetics import Algorithm
from math import cos, sinh

functions = [
    lambda x: cos(x)+sinh(x)**2,  # min at 0.0
    lambda x: (x-1)*(x+4)*(x+8)*(x-6)*(x-3)*x,  # min at -6.776, 0.4708, 5.094
    lambda x: x**4 + 9*x**3 - 5*x**2 + 2*x + 1  # should be only -7.1114
]

algorithm = Algorithm(functions[1])
# print(algorithm.calculate())
print("Local minimums at:", algorithm.find_local_minimums())


