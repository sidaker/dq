tup = (2,3)
print(type(tup))
x,y = (2,3)
print(x,y)
##x,y,z = (2,3)
##print(x,y,z)
## ValueError: not enough values to unpack (expected 3, got 2)

x,y,*z = (2,3,4,5,6,7)
print(x,y,z)

'''
Question: Which sequences can you unpack?
Any sequence (or iterable) can be unpacked into variables using a simple assignment operation.
- List
- Tuples
- Dictionaries
- Strings

'''
x,y = [2,3]
print(x,y)

x, y = {1:'a', 2:'b'}
print(x,y)

x,y,*z = 'Hello'
print(x,y,z)
