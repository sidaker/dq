# scopetest1.py
# scopetest2.py

# importing modules
import funcstobeimported
from funcstobeimported1 import scopeTest
import sys, keyword
from datetime import *
from time import *
start_timer = time()
# the above imports the functions into the programs own symbol table
funcstobeimported.echo('Sid','Python','Mac')
print(scopeTest(2))

print('Python version:',sys.version)
print('Python Interpreter Location:',sys.executable)

# list of all directories where interpreter looks for module files
for dir in sys.path:
    print(dir)


print('Python Keywords')
for word in keyword.kwlist:
    print(word)

print('Today is:', datetime.today())
print('Current hour is:', getattr(datetime.today(),'hour'))
print('Current month is:', getattr(datetime.today(),'month'))

sleep(1)

print('*' *50)
print('DICTIONARIES')
# declaring a dictionary variable
empty = { } # empty dictionary
person = { "name": "Lik Bar" }
# dictionary with one key/value pair
customer = {
"name": "Likhi",
"age": 26
} # dictionary with two key/value pairs
print(customer)

person = { "name": "Sid" }
print( person[ "name" ] )

print( person.get("name") ) # retrieves value of name key as before
print( person.get("age", "Age is not available.") ) # get is a secure way to retrieve information

# as of python, 3.7 dictionaries are ordered by default.
# in older versions of python, key-value pairs didn’t always keep their order.
# You would have needed to use an OrderedDict( ).

car = { "year": 2018 ,"model": "Mondeo"}
try:
    del car["year"]
    print(car)
except:
    print("That key does not exist")

# looping over a dictionary via the keys
person = { "name": "Sid", "age": 38 }
for key in person.keys( ):
      print(key)
      print(person[key])  # will output the value at the current key

# looping over a dictionary via the values
person = { "name": "Likhi", "age": 39 }
for value in person.values( ):
      print(value)

# looping over a dictionary via the key/value pair person = { "name": "John", "age": 26 }
for key, value in person.items( ):
    print( "{}: {}".format(key, value))

print('*' *50)
print('SETS')
'''
Sets share the same characteristics of lists and dictionaries.
A set is a collection of information like a list;
however, like a key in a dictionary, sets can only contain unique values.
They are also an unordered collection.
This means that they cannot be accessed by index but rather by the value
itself like dictionary keys.
'''

# declaring a set
s1 = set( [1, 2, 3, 1] ) # uses the set keyword and square brackets
s2 = {4, 4, 5} # uses curly brackets, like dictionary
print( type(s1), type(s2) )
s1.add(5)
s1.remove(1)
print(s1)
print(s2)
 # using the add method to add new items to a set
# using the remove method to get rid of the value 1
# notice when printed it removed the second "1" at the end

'''
Sets are mutable. Frozen sets are immutable.
Frozensets are essentially the combination of a set and a tuple.
They are immutable, unordered, and unique.
'''
print('*' *50)
print('FROZEN SETS')

# declaring a frozenset
fset = frozenset( [1, 2, 3, 4] )
print( type(fset) )



end_timer = time()

difference = round(end_timer - start_timer)

print('\nRuntime:', difference,'seconds')
