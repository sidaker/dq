
'''
How are functions first class objects in Python?

In Python, functions and classes are also treated as first-class objects.
For example, we could write the following:

'''

scream = print  # assign name ‘scream’ to the function denoted as ‘print’
print('Hello using print')
scream('Hello using scream') # call that function

'''
we have simply defined scream as an alias for the existing print function.
'''
