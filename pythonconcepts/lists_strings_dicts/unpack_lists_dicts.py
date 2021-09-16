# A Python program to demonstrate need
# of packing and unpacking

# A sample function that takes 4 arguments
# and prints them.
def fun(a, b, c, d):
	print(a, b, c, d)

# Driver Code
my_list = [1, 2, 3, 4]

# This doesn't work
#fun(my_list)

# Unpacking list into four arguments
fun(*my_list)


print(range(3, 6))  # normal call with separate arguments
[3, 4, 5]
args = [3, 6]
print(range(*args))  # call with arguments unpacked from a list
