'''
A function is a block of code which only runs when it is called.
You can pass data, known as parameters, into a function.
A function can return data as a result
'''

# writing basic function.No Arguments.No explicit return
def printInfo( ): # defines what the function does when called
    print("Name: Lik Gangi")
    print("Age: 33")

# passing a single parameter into a function.No explicit return
def printName(full_name):
    print( "Your name is: {}".format(full_name) )

# passing multiple parameters into a function
def addNums(num1, num2):
    result = num1 + num2
    return( "{} + {} = {}".format(num1, num2, result) )

# passing a multiple parameters into a function.No explicit return
# setting default parameter values
def printNamewithSalute(full_name='Advik',Salutation='Master'):
    print( "Your name is: {} {}".format(Salutation,full_name) )

# passing a list as an argument
def squares(nums):
    squarelist = []
    for num in nums:
        squarelist.append(num**2)
    return squarelist

'''
The use of *args allows you to pass a variable number of arguments into a function. This
allows you to make functions more modular. The magic isn’t the “args” keyword here
though; it’s really the unary operator (*) that allows us to perform this feature. You could
theoretically replace the word args with anyone, like “*data”, and it would still work.
However, args is the default and general standard throughout the industry.
'''

# Build a function that can take variable number of parameters.
# using args parameter to take in a tuple of arbitrary values
def outputData(name, *args):
    print( type(args) )
    for arg in args:
        print(arg)

'''
Like args, kwargs allows us to take in an arbitrary number of values in a function;
however, it works as a dictionary with keyword arguments instead. Keyword arguments
are values passed in with keys, which allow us to access them easily within the function
block. Again, the magic here is in the two unary operators (**) not the keyword of
kwargs.
'''

# using kwargs parameter to take in a dictionary of arbitrary values
def outputDatakw(**kwargs):
    print( type(kwargs) )
    print( kwargs[ "name" ] )
    print( kwargs[ "num" ] )



printInfo( ) # calls the function to run
printInfo( ) # calls the function again

printName("Lik Gangi")
printName("Bar")

print(addNums(5, 8)) # will output 13
print(addNums(3.5, 5.5)) # will output 9.0

numbers1 = [ 2, 4, 5, 10 ]
numbers2 = [ 1, 3, 6 ]
print(squares(numbers1))
print(squares(numbers2))

printNamewithSalute()
printNamewithSalute('Gangireddy','Miss')
printNamewithSalute('Gangireddy')

# This is a useful mechanism when you’re not sure how many arguments to expect.
outputData("L GREDDY", 5, True, "Data Engineer")
outputData("M BREDDY", 5)

outputDatakw(name = "L GREDDY", num = 5, b = True)
outputDatakw(name = "M BREDDY", num = 5, b = True, x = "Data Engineer")
