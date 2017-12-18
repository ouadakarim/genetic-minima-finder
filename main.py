import sys
import parser
import re
from genetics import Algorithm

POLYNOMIAL_REGEX=r"(^-)?(((\d+(\.\d+)?)?(x(\^\d)?)?)([+-](?!$))?)*"
DEFAULT_MIN_X = -100
DEFAULT_MAX_X = 100

def int_input(msg, default):
	inp = input(msg)
	if not inp:
		return default
	try:
		return int(inp)
	except:
		print("Not an integer")
		sys.exit(-1)

print("Provide polynomial to analyze")
print("Example: -1.23x^4")
user_input = input(">> ")

if not re.fullmatch(POLYNOMIAL_REGEX, user_input):
	print("Provided function is not valid polynomial of variable x")
	sys.exit(-1)

min_x = int_input("Provide start of evalution range (min x, default -100): ", DEFAULT_MIN_X)
max_x = int_input("Provide end of evalution range (max x, default 100): ", DEFAULT_MAX_X)

if min_x >= max_x:
	print("Min x has to be smaller than max x")
	sys.exit(-1)

user_input = "lambda x: " + user_input.replace("^", "**")
user_input = re.sub(r"\dx", lambda mo: mo.group(0)[0]+"*x", user_input)

function_st = parser.expr(user_input).compile()
function = eval(function_st)

algorithm = Algorithm(function)
result = algorithm.find_local_minimums(min_val=min_x, max_val=max_x)
if result:
	print("Local minima at:", result)
else:
	print("No local minima found in analyzed range!")
