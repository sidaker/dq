from functools import reduce

def add10(x):
    return x+10
def exectwice(fun,x):
    return(fun(fun(x)))

print(exectwice(add10,30))

# lambda function has no name and no return statement
#1 way of calling lambda
funlambda = lambda x: x**3
print(funlambda(3))
print(funlambda(4))
#2nd way of calling lambda
print((lambda x: x**4)(2))

# map
lista = [2,10,20,30,40,9]

mapresult = map(funlambda,lista)
print(type(mapresult))
print(mapresult)
print(list(mapresult))

# filter

filterresult = filter(lambda x: x>15,lista)
print(type(filterresult))
print(filterresult)
print(list(filterresult))

# reduce
def do_sum(x1, x2): return x1 + x2

print(reduce(do_sum, [1, 2, 3, 4,5]))
print(reduce(lambda x,y: x*y, [1, 2, 3, 4,5]))
