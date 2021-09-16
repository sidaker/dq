# A sample program to demonstrate unpacking of
# dictionary items using **
def fun(a, b, c):
	print(a, b, c)

# A call with unpacking of dictionary
d = {'a':2, 'b':4, 'c':10}
fun(**d)
'''
Here ** unpacked the dictionary used with it, and passed the items in the
dictionary as keyword arguments to the function.

'''
## fun(22, **d)
## TypeError: fun() got multiple values for argument 'a'

# A Python program to demonstrate packing of
# dictionary items using **
def fun(**kwargs):

	# kwargs is a dict
	print(type(kwargs))

	# Printing dictionary items
	for key in kwargs:
		print("%s = %s" % (key, kwargs[key]))

# Driver code
fun(name="Advik", ID="101", language="Python")
