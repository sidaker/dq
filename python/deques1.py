import collections
import string

'''

'''

def main():
    d =  collections.deque(string.ascii_lowercase)
    print(len(d))

    for elem in d:
        print(elem.upper(),end=",")
    print("\n")
    # pop from either side of deque
    #
    d.pop()
    d.popleft()
    print(d)
    d.append(2)
    d.appendleft(1)
    print(d)

    # rotate the deque
    d.rotate(10) # value on the end goes to front
    print(d)
    d.rotate(1)
    print(d)


if __name__ == '__main__':
    main()
