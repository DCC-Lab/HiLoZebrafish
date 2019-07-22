from math import sqrt, log, exp
from sympy import symbols, solve, Function, Eq, solveset

# a =	66377.8508
# b = 3.93834
# c = 0.71691
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

<<<<<<< Updated upstream
a =	91.2742
b =	95.32937
c = 1023.99992
d = 128.54601
=======
a = 87.84735
b = 98.01746
c = 1024.00005
d = 242.19578
>>>>>>> Stashed changes
y = (b-a)/2 + a
x = symbols('x', real=True)

f = ((-1 / (2 * d**2)) * x**2) + (((c / d**2) ) * x) - (c**2 / (2 * d**2)) - log((y-a) / (b-a))


solutions = solve(f, x)


FWHM = solutions[1] - solutions[0]


print(a, b, c, d, solutions[0], solutions[1], FWHM, sep=' ')