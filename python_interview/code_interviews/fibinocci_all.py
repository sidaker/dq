def fib1(n):
    if n in (0,1):
        return n
    else:
        return fib1(n-1)+fib1(n-2)

def fib2(n):
    cache = {0:0,1:1}
    if n in cache:
        return cache[n]
    else:
        cache[n] = fib1(n-1)+fib1(n-2)
        return cache[n]

def get_fib_series(n):
    a,b,i = 0,1,0
    yield a
    while True:
        a, b , i = b, a+b , i+1
        yield a
        if(n==i):
            break


def get_nth_fib_no(n):
    if n<2:
        return n
    return get_nth_fib_no(n-1) + get_nth_fib_no(n-2)


class Fib():
    def __init__(self, howMany):
        self.counter = howMany
        self.curFib  = 0
        self.nextFib = 1

    def __iter__(self):
     #  Creates iterator object
     #  Called when iteration is initialized
     #  Called during initialization
     #  Return an object that exposes an __next__ method.
     #  self (whose type is Fibonacci) is such an object:
     #
        return self

    def __next__(self):

        if self.counter == 0:
        #
        #  We have returned the count of fibonacci numbers
        #  asked for… stop the iteration:
        #
           raise StopIteration

        self.counter -= 1
        result  = self.curFib
        nextFib       = self.curFib + self.nextFib
        self.curFib   = self.nextFib
        self.nextFib  = nextFib

        return result


if __name__ == '__main__':
    import timeit

    for i in get_fib_series(9):
        print(i, end=" ")

    print("*"*50)

    fib_10 = Fib(10)
    for i in fib_10:
        print(i, end=" ")

    assert fib1(0) == 0
    assert fib1(1) == 1
    assert fib1(2) == 1
    assert fib1(3) == 2

    assert fib2(0) == 0
    assert fib2(1) == 1
    assert fib2(2) == 1
    assert fib2(3) == 2
    assert fib2(4) == 3
