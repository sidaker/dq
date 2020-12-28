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


if __name__ == '__main__':
    # Fibonacci Sequence is the series of numbers: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
    print(get_nth_fib_no(0))   # 0
    print(get_nth_fib_no(1))   # 1
    print(get_nth_fib_no(2)) # 1
    print(get_nth_fib_no(3)) # 2
    print(get_nth_fib_no(4)) # 3
    get_nth_fib_no(5) # 4

    print("***")
    for i in get_fib_series(9):
        print(i, end=" ")
