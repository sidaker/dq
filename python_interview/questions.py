def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_whee():
    print("Whee!")

'''
So, @my_decorator is just an easier way of saying
say_whee = my_decorator(say_whee). It’s how you apply a decorator to a function.
'''


'''
Differences between Generator function and Normal function

Generators in Python (also called generator functions) are used to create a series of values one at a time.

Generator function contains one or more yield statements.
When called, it returns an object (iterator) but does not start execution immediately.
Methods like __iter__() and __next__() are implemented automatically. So we can iterate through the items using next().

The easiest ways to make our own iterators in Python is to create a generator.

range is implemented as a generator to save memory.

https://inventwithpython.com/blog/2021/09/24/what-is-a-python-generator-implementing-your-own-range-function/

To run the code inside a generator function, you must call Python's built-in next() function and pass it the generator object. This will run the code up until a yield statement, which acts like a return statement and makes the next() call return a value. The next time next() is called, the execution resumes from the yield statement with all the same values for the local variables.

When a return statement is reached, the generator function raises a StopIteration exception. Usually there's no value returned, but if so it is set to the exception object's value attribute.


'''

'''
Iterable is an object, which one can iterate over.
It generates an Iterator when passed to iter() method.
Iterator is an object, which is used to iterate over an iterable object using __next__() method.

When a for loop is executed, for statement calls iter() on the object, which it is supposed to loop over.
If this call is successful, the iter call will return an iterator object that defines the method __next__()
'''

print(type(range(10)))
for i in range(10):
    print(i)
