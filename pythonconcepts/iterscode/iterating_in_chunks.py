import itertools
# This type of code is useful when you want to pass a fixed size  list everytime you call an API.
# Example to drop glue partitions, the API has a limit of 25 partitions per call.


def chunked_iterable(iterable, size):
    it = iter(iterable)
    # above ensures that the value variable it is using the same iterator throughout
    # If you pass certain fixed iterables to islice(), it creates a new iterator each time.
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


if __name__ == '__main__':
    for c in chunked_iterable(range(14), size=4):
        print(c)

        # (0, 1, 2, 3)
        # (4, 5, 6, 7)
        # (8, 9, 10, 11)
        # (12, 13)
