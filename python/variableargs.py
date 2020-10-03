# variable argument lists
# variable args has to be the last argument after all positional parameters
# e.g. def logm(mtype, msg, *params)

def addition(*args):
    sum=0
    for i in range(len(args)):
        sum += args[i]
    return sum


def add2(x,y,*,ops='add'):
    if(ops == 'add'):
        return x+y
    else:
        return x*y


if __name__ == '__main__':
    print(addition(2,3))
    print("*"*50)
    print(addition(2,3,4))
    # Pass a list directly.
    list1 = [1,3,6,10,45,6,9,20]
    print(addition(*list1))
    print(add2(2,4,ops='add'))
    print(add2(2,4,ops='zzz'))
