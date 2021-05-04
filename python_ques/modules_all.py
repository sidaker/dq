import math

for mod in dir(math):
    print(mod, end="\t")

print("\n")
from random import random, seed, randrange, randint

print(randrange(1), end=' ')
print(randrange(0, 1), end=' ')
print(randrange(0, 10, 1), end=' ')
print(randint(0, 10)) # no right sided exclusion

print("*"*50)
for i in range(5):
    print(random())

print("*"*50)
seed(0)
'''
0.8444218515250481
0.7579544029403025
0.420571580830845
0.25891675029296335
0.5112747213686085
'''

for i in range(5):
    print(random())


from random import choice, sample

my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(choice(my_list))
print(sample(my_list, 5))
print(sample(my_list, 10))

from random import choice, sample

my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(choice(my_list))
print(sample(my_list, 5))
print(sample(my_list, 10))

from platform import platform

print(platform())
print(platform(1))
print(platform(0, 1))


from platform import machine, processor,system,version,python_implementation, python_version_tuple

print(python_implementation())

for atr in python_version_tuple():
    print(atr)

print(machine())
print(processor())
print(system())
print(version())


import sys

for p in sys.path:
    print(p)
