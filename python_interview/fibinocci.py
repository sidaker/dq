def fibonacci( ):
    # 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
    a = 0
    b = 1
    while True:            # keep going. . .
        yield a              # report value, a, during this pass
        future = a + b
        a = b                # this will be next value reported
        b = future           # and subsequently this

def fibonacci_simplified():
    print(dir()) # function, dir, reports the names of the identifiers in a given namespace (i.e., the keys of the dictionary)
    a, b = 0, 1
    print(dir())
    print(vars()) # function, vars, returns the full dictionary
    print(a.__dir__) # each object has its own namespace to store its attributes
    while True:
        yield a
        a, b = b, a+b


if(__name__ == '__main__' ):

    for ct,i in enumerate(fibonacci()):
        print(i)
        #print(ct)
        if(ct > 5):
            break

    print("*"*50)

    for ct,i in enumerate(fibonacci_simplified()):
        print(i)
        #print(ct)
        if(ct > 7):
            break
