
name1 = "Bargu"
name2 = 'Likhi'
s = "Look over that way"
# create a top border
print( "*" * 50 )
# using the new f strings from python 3.6
print( f"Hello {name1}")
print('Hello, %s' % name2)
# finding the starting index of our searched term
print( s.find("over") )
print( "*" * 50 )
dict1 = {1:"sid",2:"likhi",3:"Advik"}

try:
    print(dict1[4])
except:
    print("Error has Occured ")

print( "*" * 50 )

try:
    print(dict1[3])
except:
    print("Error has Occured ")

print( "*" * 50 )

try:
    print(dict1[4])
except KeyError:
    print("Unknown ID. ID does not exist ")
finally:
    print("This will be printed no matter what")

x, y = 5, 10
if x > y:
 print("x is greater")
elif x < y:
 print("x is less")

# declaring a list of mixed data types
num = 4.3
data = [num, "word", True] # the power of data collection
print(data)

# understanding lists within lists
data = [5, "book", [ 34, "hello" ], True] # lists can hold any type
print(data)
print( data[2])

# using [:] to copy a list
data = [5, 10, 15, 20]
data_copy = data[ : ] # a single colon copies the list
data[0] = 50
print( "data: {}\t data_copy: {}".format(data, data_copy))

# writing your first for loop using range
for num in range(5):
 print( "Value: {}".format(num))

# providing the start, stop, and step for the range function
for num in range(2, 10, 2):
 print( "Value: {}".format(num) ) # will print all evens between 2 and 10
