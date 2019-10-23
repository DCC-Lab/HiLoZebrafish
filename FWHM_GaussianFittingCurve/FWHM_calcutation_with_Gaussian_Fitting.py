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

a = 91.19781
b = 93.15748
c = 1023.91617
d = 33.93568

y = (b-a)/2 + a
x = symbols('x', real=True)

f = ((-1 / (2 * d**2)) * x**2) + (((c / d**2) ) * x) - (c**2 / (2 * d**2)) - log((y-a) / (b-a))


solutions = solve(f, x)


FWHM = (solutions[1] - solutions[0]) / 2


print(a, b, c, d, solutions[0], solutions[1], FWHM, sep='\t')