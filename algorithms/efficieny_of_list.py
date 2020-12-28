from timeit import Timer
# https://runestone.academy/runestone/books/published/pythonds/AlgorithmAnalysis/Lists.html
'''
Two common list operations are indexing and assigning to an index position.
Both of these operations take the same amount of time no matter how large the
list becomes. When an operation like this is independent of the size of the list
 they are 𝑂(1).
'''

'''
Efficieny 1:
Appending is faster than concatenation.
Append is even faster than insert.
There are two ways to create a longer list.
You can use the append method or the concatenation operator.
The append method is 𝑂(1).
However, the concatenation operator is 𝑂(𝑘) where 𝑘 is the size of the list
that is being concatenated.
'''

def test1():
    # list creation by concatenation.
    l = []
    for i in range(1000):
        l = l + [i]

def test2():
    # list creation by append.
    l = []
    for i in range(1000):
        l.append(i)

def test3():
    # list creation using list comprehension and range.
    l = [i for i in range(1000)]

def test4():
    # range function wrapped by a call to the list constructor.
    l = list(range(1000))


if __name__ == '__main__':
    # imports the function test1 from the __main__ namespace into the namespace that timeit sets up for the timing experiment. 
    t1 = Timer("test1()", "from __main__ import test1")
    print("concat ",t1.timeit(number=1000), "milliseconds")
    # The timeit module will then time how long it takes to execute the
    # statement some number of times.
    # By default timeit will try to run the statement one million times.
    t2 = Timer("test2()", "from __main__ import test2")
    print("append ",t2.timeit(number=1000), "milliseconds")
    t3 = Timer("test3()", "from __main__ import test3")
    print("comprehension ",t3.timeit(number=1000), "milliseconds")
    t4 = Timer("test4()", "from __main__ import test4")
    print("list range ",t4.timeit(number=1000), "milliseconds")
    t5 = Timer("test4()", "from __main__ import test4")
    print("list range ",t4.timeit(), "microseconds") # executes a million times

'''
To capture the time it takes for each of our functions to execute we will use
Python’s timeit module.
The timeit module is designed to allow Python developers to make cross-platform
timing measurements by running functions in a consistent environment and using
timing mechanisms that are as similar as possible across operating systems.
'''
