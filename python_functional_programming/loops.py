x = 10
while(x := x -1) > 5:
    print(x,  end='')

print('\n')
print(bool(set()))

strtest = 'Hello'
print(strtest.encode("UTF-8"))



def add(*args):
    '''
    add functions takes variable number of arguments
    '''
    res = 0
    for arg in args:
        res += arg
    return res

print(add(2,3,4))
print(add(10,2))

## use literal unpacker
lista = [1,2,3,4,5]
print(add(*lista))
##print(add(lista))  ## TypeError

def myfunc(arg1,arg2, *, suppress_exc=False):
    '''
    Takes 2 positional parameters,
    Third is a mandatory keyword
    '''
    print("executed")

try:
    myfunc(2,3,True)
except TypeError:
    print("Please pass the 3rd argumnet as keyword")
    myfunc(2, 3, suppress_exc=True)