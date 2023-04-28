import collections

#print(str.__doc__)
#print(collections.__doc__)

def myfunc(arg1, arg2=None):
    """
    my func takes 2 arguments. the 2nd is optional.
    Parameters:
        arg1: first argument
        arg2: entirely optional
    """
    print(arg1, arg2)

print(myfunc.__doc__)