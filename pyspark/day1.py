
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

# printing all characters in a name using the 'in' keyword
name = "Lik Bar"
for letter in name:
 print( "Value: {}".format(letter) )

# A while loop is generally used when
# you need to loop based on a condition rather than counting.

# using two or more loops together is called a nested loop
for i in range(2): # outside loop
    for j in range(3): # inside loop
        print( i, j )

# checking the number of items within a list
nums = [5, 10, 15]
length = len(nums) # len() returns an integer
print(length)

# accessing specific items of a list with slices
print( nums[ 1 : 3 ] ) # will output items in index 1 and 2
print( nums[ : 2 ] ) # will output items in index 0 and 1
print( nums[ : : 2 ] ) # will print every other index - 0, 2, 4, etc.
print( nums[ -2 : ] ) # will output the last two items in list

# using the remove method with a try and except
sports = [ "baseball", "soccer", "football", "hockey" ]
try:
    sports.remove("soccer")
except:
    print("That item does not exist in the list")
print(sports)


# using min, max, and sum
nums = [5, 3, 9]
print( min(nums) ) # will find the lowest number in the list
print( max(nums) ) # will find the highest number in the list
print( sum(nums) ) # will add all numbers in the list and return the sum


# using sorted on lists for numerical and alphabetical data
nums = [5, 8, 0, 2]
sorted_nums = sorted(nums) # save to a new variable to use later
print(nums, sorted_nums) # the original list is in tact


# sorting a list with .sort() in-place
'''
The sort method is used for the same purpose that our previous sorted function is used
for; however, it will change the original list directly:
'''
nums = [5, 0, 8, 3]
nums.sort( ) # alters the original variable directly
print(nums)

# using conditional statements on a list
names = [ "Jack", "Robert", "Mary" ]
if "Mary" in names:
    print("found") # will run since Mary is in the list
if "Jimmy" not in names:
    print("not found") # will run since Jimmy is not in the list

# using conditionals to see if a list is empty
nums = [ ]
if not nums: # could also say 'if nums == []'
    print("empty")


# using a for loop to print all items in a list
sports = [ "Baseball", "Hockey", "Football", "Basketball" ]
for sport in sports:
    print(sport)
