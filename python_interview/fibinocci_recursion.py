def fib1(n):
    # Recursion should have an base or end condition.
    # 0,1,1,2,3,5,8,13
    if n < 2:
        return n
    return fib1(n - 1) + fib1(n - 2)

def nonrecfib(n):
    #
    a, b, i = 0, 1 , 0
    while True:
        yield a
        i += 1
        if(i>=n):
            break
        a, b = b, a+b

if __name__ == "__main__":
    print(fib1(1))
    print(fib1(5))
    print(fib1(6))
    print(fib1(7))

    print("*****")

    for i in nonrecfib(9):
        print(i)
