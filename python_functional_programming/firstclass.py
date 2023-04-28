## Composition
def f(x):
    return x + 2

def g(h, x):
    return h(x) * 2

print(g(f,42))

## Closure
'''
in simple terms: A closure is an inner function that remembers and has access to variables in the 
local scope in which it was created even after the outer function has finished executing"
'''
def addx(x):
    def _(y):
        return x+y
    return _

add2 = addx(2)
add3 = addx(3)

print(add2(20), add3(3))

## Currying.
def f(x,y):
    return x*y

def f2(x):
    def _(y):
        return f(x,y)
    return _

print(f2(2))
print(f2(2)(3))