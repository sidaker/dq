import itertools


def chunked_iterable(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


genobj=chunked_iterable([1,2,3,4,5,6,7],size=2)

# generator functions are a special kind of function that return a lazy iterator.
# These are objects that you can loop over like a list. However, unlike lists, lazy iterators do not store their contents in memory.

for n in genobj:
    print(n)
