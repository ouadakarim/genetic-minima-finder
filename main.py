import sys
import parser
import re
from genetics import Algorithm

POLYNOMIAL_REGEX=r"(^-)?(((\d+(\.\d+)?)?(x(\^\d)?)?)([+-](?!$))?)*"

print("Provide polynomial to analyze")
print("Example: -1.23x^4")
user_input = input()

if not re.fullmatch(POLYNOMIAL_REGEX, user_input):
	print("Provided function is not valid polynomial of variable x")
	sys.exit(-1)

user_input = "lambda x: " + user_input.replace("^", "**")
user_input = re.sub(r"\dx", lambda mo: mo.group(0)[0]+"*x", user_input)

function_st = parser.expr(user_input).compile()
function = eval(function_st)

algorithm = Algorithm(function)
# print(algorithm.calculate())
print("Local minimums at:", algorithm.find_local_minimums())


