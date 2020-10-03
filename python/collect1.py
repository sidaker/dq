import collections
from collections import defaultdict

'''
lists -> mutable
tuples-> immutable
sets -> unordered, sequence of distinct values.mutable.

named tuples -> Tuples with named fields.
ordered Dict, defasult Dict ->
Counter
deque -> Double ended list
'''

def idefaultdict11():
    fruits = ['rasperry','apple','banana','pear','mango','pear','strawberry','apple','banana']
    fruitcounter = defaultdict(int) # creates a default value.
    #fruitcounter = defaultdict(lambda: 100) # default startts at 100
    for f in fruits:
        fruitcounter[f] += 1
    print(fruitcounter)
    return fruitcounter




def tupll():
    tup1 = 1,2,3,4
    print(tup1)
    print(type(tup1))
    print(tup1[0])
    print(tup1[1])

    Point=  collections.namedtuple("Point","x y")
    p1 = Point(10,20)
    p2 = Point(2,3)
    print(p1,p2)
    print(p1.x,p2.y)
    # play with gemoetry like this.
    # use _replace to create a new instance.
    p1 = p1._replace(x=100)
    print(p1)

def main():
    tupll()
    idefaultdict11()




if __name__ == '__main__':
    main()
