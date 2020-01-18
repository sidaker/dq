# where global variables can be accessed
def scopeTest1():
    try:
        number += 1 # not accessible due to function level scope
        # Error: local variable 'number' referenced before assignment
    except Exception as e:
        print(e)

try:
    number = 5
    scopeTest1()
except Exception as e:
    print(e)
