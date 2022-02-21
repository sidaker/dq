from itertools import count, chain, cycle

def iter1():
    c = count()
    print(next(c))
    print(next(c))
    print(next(c))
    # you can go on

def iter2():
    d = cycle([1,2,3])
    print(next(d))
    print(next(d))
    print(next(d))
    print(next(d))

def iter3():
    e = chain([1,2],{'adv:1'},[4,5,6],{'sid:1'})
    print(next(e))
    print(next(e))
    print(next(e))
    print(next(e))

def gen1(n):
    '''
    Generator functions are distinguished from plain old functions by the
    fact that they have one or more yield statements.
    The easiest ways to make our own iterators in Python is to create a generator.
    '''
    for i in  range(n):
        yield i

if __name__ == '__main__':
    iter1()
    print("*"*50)
    iter2()
    print("*"*50)
    iter3()
    print("*"*50)
    genobj = gen1(5)
    print(type(genobj))
    print(genobj)

    for j in genobj:
        print(j)
