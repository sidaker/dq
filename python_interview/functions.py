# Python's import statement loads definitions from a module into the current namespace.
# This command adds both pi and sqrt, as defined in the math module, into the current namespace, allowing direct use of the identifier, pi, or a call of the function, sqrt
from math import pi, sqrt
import fibinocci

# max function
a = 2
b = -3
print(max(a, b))
print(max(a, b, key=abs))

print(pi)
print(sqrt(4))

# print(fibonacci_simplified())
# Above will not work. NameError: name 'fibonacci_simplified' is not defined
# use from fibinocci import fibonacci_simplified for it to work.
print(fibinocci.fibonacci_simplified())
for i in fibinocci.fibonacci_simplified():

    if(i > 10):
        break
    print(i)
