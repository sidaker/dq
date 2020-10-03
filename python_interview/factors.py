# generator that computes factors
def factors(n):


    '''
    Implements factors as a generator
    '''
    k = 1
    while k * k < n:        # while k < sqrt(n)
        if n % k == 0:
            yield k
            yield n // k
        k += 1
    if k * k == n:          # special case if n is perfect square
        yield k



if(__name__ == '__main__' ):
    for i in factors(100):
        print(i)
