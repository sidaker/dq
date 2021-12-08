def outer():
    x = "local"

    def inner():
        nonlocal x
        x = "nonlocal"
        print("inner:", x)

    inner()
    print("outer:", x)


outer()

def f():
    '''
    We can see that the global statement inside the nested function g does not affect the variable 'city' of the function f, i.e. it keeps its value 'Hamburg'. We can also deduce from this example that after calling f() a variable 'city' exists in the module namespace and has the value 'Geneva'. This means that the global keyword in nested functions does not affect the namespace of their enclosing namespace!
    A variable defined inside of a function is local unless it is explicitly marked as global. In other words, we can refer to a variable name in any enclosing scope, but we can only rebind variable names in the local scope by assigning to it or in the module-global scope by using a global declaration. We need a way to access variables of other scopes as well. The way to do this are nonlocal definitions
    '''
    city = "Hamburg"
    def g():
        global city
        city = "Geneva"
    print("Before calling g: " + city)
    print("Calling g now:")
    g()
    print("After calling g: " + city)

f()
print("Value of city in main: " + city)
