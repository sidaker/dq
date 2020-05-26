import func_2
'''
Pythons object model
Named References to objects
Value vs identity equality.
Passing arguments and returning values.
Dynamically typed vs Statically typed
'''

'''
id() returns a unique integer identifier for an object
that is constant for the life of the object.
'''

a = 100
b = 100
c= 22
print(id(a))
print(id(b))
print(id(c))

if a is b:
    print("a and b refer to same object")

'''
Value Equality vs Identity equality'''

p = [1,4,9,7]
q = [1,4,9,7]

if p == q:
    print("Values are equal")

if p is q:
    print("Identity is Equal")
else:
    print("Identity is not equal")

'''
Function arguments are transferred using pass-by-object-reference.
References to objects are copied, not the objects themselves.
Call by reference.
Python uses pass by reference.

Always use immutable objects for function argument defaults.
Python has dynamic and strong type system.
Java has a static type system.

What is enclosing scope in python?
Why rebind global names
'''
count=0
couuntg=0

def set_count(c):
    global couuntg
    couuntg = c
    count = c

def show_count():
    print(count)
    print(couuntg)

show_count()
set_count(5)
print("***")
show_count()

print(dir(func_2))
