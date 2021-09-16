import pytest

# Function with variable number of arguments.
def multiadd(*args):
    result = 0
    for i in args:
        result = result + i
    return result

def multiadd2(a,*args):
    result = a*2
    for i in args:
        result = result + i
    return result

if(__name__ == "__main__"):
    print(multiadd(1,2,3,4))
    assert multiadd(1,2,3,4) == 10
    assert multiadd(11,20,19) == 50
    assert multiadd(11,29,10,50,100) == 200
    assert multiadd(11,2) == 13
    assert multiadd(11) == 11

    assert multiadd2(11,2,3,4) == 31
    assert multiadd2(10,5,5) == 30
