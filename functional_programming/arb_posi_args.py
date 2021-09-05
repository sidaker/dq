def hypervol(*args):
    i = iter(args)
    vol = next(i)
    for len in i:
        vol *=  len
    return vol


def hypervol1(arg, *args):
    '''
    When you need to accept a variable number of arguments with a positive lower bound you should consider this practice of using regular positional arguments for the required parameters and *args to deal with any extra arguments. Note that *args must come after any normal positional arguments and that there can only be one occurrence of *args within the argument list. The *args syntax only collects positional arguments and a complimentary syntax is provided for handling keyword arguments. 
    '''
    vol = arg
    for len in args:
        vol *=  len
    return vol

if __name__=='__main__':
    print(hypervol(2,3))
    print(hypervol(2,3,4))
    print(hypervol(2,3,4,5))
    #print(hypervol())
    print("*******")
    print(hypervol1(2,3))
    print(hypervol1(2,3,4))
    print(hypervol1(2,3,4,5))
    print(hypervol1())
