'''
Use map and filter over a collection

'''

from functools import reduce

lista = [ 1,2,3,45,6]

lambda_func = lambda x: x**2

listb =  map(lambda_func, lista)

print(listb)

print(list(listb))

listb = filter(lambda n: n>5, lista)

print(listb)

print(list(listb))


var_reduce = reduce(lambda acc, n: n+acc, lista, 0)

print(var_reduce)

