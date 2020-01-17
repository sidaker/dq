'''
Types of scope
    function
    global
    class

'''
'''
When global attributes are defined, they’re accessible to the rest of the file. However, we
must keep in mind how function scope works. Even when you declare a variable accessible
to the entire file, it will not be accessible within the function.
When dealing with variables declared in a function, you generally won’t need to access
it outside of the function. However, in order to access that value, best practice is to
return it:
'''

# where global variables can be accessed
number = 5
def scopeTest():
    try:
        number += 1 # not accessible due to function level scope
        # UnboundLocalError
    except Exception as e:
        print(e)

# call by value vs call by reference
num = 5
def changeNum(num):
    num += 5

print(num)
print('*' *50)
changeNum(num)
print("Value of num does not change")
print(num)

'''
This is different when changing information via index though. Due to how index’s
work, via memory location and not by reference, changing an element in a list by the
index location will alter the original variable
'''

# changing list item values by index
sports = [ "baseball", "football", "hockey", "basketball" ]
def change(aList):
    aList[ 0 ] = "soccer"

print("Before Altering: {}".format(sports) )
change(sports)
print( "After Altering: {}".format(sports) )



# When passed in, it only passes the value, not the variable.
scopeTest()
