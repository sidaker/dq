from functools import reduce

def add10(x):
    return x+10
def exectwice(fun,x):
    return(fun(fun(x)))

print(exectwice(add10,30))

print(add10.__code__.co_varnames)

# lambda function has no name and no return statement
#1 way of calling lambda. making function a callable object.
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

year_sales=[(2000,102),(2001,220),(2002,340),(2003,50),(2004,90)]

print(max(year_sales))
# max is a higher order functions. So you can apply function to it as an argument
print(max(year_sales,key=lambda x:x[1]))
