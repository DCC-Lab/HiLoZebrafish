from math import sqrt, log, exp
from sympy import symbols, solve, Function, Eq, solveset

# a =	8011.5307
# b = 967.49638
# c = 1226.38038
# print(a, b, c, sep='\n')
#
# y = a/2
# print(y)
# x = symbols('x', real=True)
#
# f = (-(1 / (2*c**2)) * x**2) + ((b/c**2) * x) + (-(b**2 / (2*c**2)) - log(y/a))
# print(f)
#
# solutions = solve(f, x)
# print(solutions)
#
# FWHM = solutions[1] - solutions[0]
# print(FWHM)



# stddev = 1247.11445
# fwhm = 2 * stddev * sqrt(2 * log(10))
# print(fwhm)

'''Gaussian fit curve'''


a =	3415.57639
b =	8047.43809
c = 965.19833
d = 871.13712

y = (b-6005)/2 + 6005
x = symbols('x', real=True)

f = ((-1 / (2 * d**2)) * x**2) + (((c / d**2) ) * x) - (c**2 / (2 * d**2)) - log((y-a) / (b-a))


solutions = solve(f, x)


FWHM = (solutions[1] - solutions[0]) / 2


print(a, b, c, d, solutions[0], solutions[1], FWHM, sep=' ')