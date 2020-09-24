'''
-- Syntax of for loop.
for element in iterable:

There are many types of objects in Python that qualify as being
iterable.
Basic container types, such as list, tuple, and set, qualify as
iterable types.

Furthermore,
a string can produce an iteration of its characters,
a dictionary can produce an iteration of its keys,
a file can produce an iteration of its lines.
User-defined types may also support iteration.

In Python, the mechanism for iteration is based upon the following conventions:

•	An iterator is an object that manages an iteration through a series of values. If variable, i, identifies an iterator object, then each call to the built-in function, next(i), produces a subsequent element from the underlying series, with a StopIteration exception raised to indicate that there are no further elements.
•	An iterable is an object, obj, that produces an iterator via the syntax iter(obj).

By these definitions, an instance of a list is an iterable,
but not itself an iterator.
With data = [1, 2, 4, 8], it is not legal to call next(data).
However, an iterator object can be produced with syntax, i = iter(data), and then each subsequent call to next(i) will return an element of that list. The for-loop syntax in Python simply automates this process, creating an iterator for the give iterable, and then repeatedly calling for the next element until catching the StopIteration exception.

'''
data = [1, 2, 4, 8]
print(type(data)) # <class 'list'>

for i in data:
    print(i)

# Let us produce an iterable object from a list.
iobj = iter(data)
print(type(iobj)) # <class 'list_iterator'>
print("Calling next()")
print(next(iobj)) # prints 1
# print(next(data)) # This is illeagal. data

print("loop over the remaining iterable object")
for i in iobj:
    print(i) # print 2,4,8. 1 is already printed and spent.

print("Try after the iterator is spent")
for i in iobj:
    print("Nothing to print")
    print(i)

# print(next(data))
# data is a list and hence is an iterator but to iterate
# you need to create an iterable from the list.
# iter(data) does exactly that. Creates an iterator.
print(next(iter(data)))

v_try_it = iter([1,2])
print(next(v_try_it))
print(next(v_try_it))
# print(next(v_try_it)) # produces StopIteration exception.

'''
That iterator does not store its own copy of the list of elements. Instead, it maintains a current index into the original list, representing the next element to be reported. Therefore, if the contents of the original list are modified after the iterator is constructed, but before the iteration is complete, the iterator will be reporting the updated contents of the list.
'''
