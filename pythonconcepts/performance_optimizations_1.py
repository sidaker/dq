# measuring code time.
from time import perf_counter
from timeit import timeit

items = { 'a': 1,'b':2}
def getsum(n):
    return sum(range(n))

def use_get(key):
    return items.get(key,-1)

if __name__ == '__main__':
    n = 100000

    start = perf_counter()
    print(start)
    getsum(n)
    duration = perf_counter() - start
    print("Duration:", duration)

    print('get:',timeit('use_get("x")','from __main__ import use_get '))
