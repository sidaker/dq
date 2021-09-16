import itertools
# Use it to generate iterators.
# Module implements a number of iterator building blocks.

def testFunc(x):
    return x< 40

def main():
    # cycle over a collection.
    seq1 = ["sid","adv","lik"]
    cycle1 = itertools.cycle(seq1)
    for i,j in enumerate(cycle1):
        print(i,j)
        if(i==5):
            break

    # count iterator.
    count1 =itertools.count(100,10)
    for i,j in enumerate(count1):
        print(i,j)
        if(i==5):
            break

    # accumulator iterator.
    # unlike cycle and count this is not an infinite iterator
    vals = [10,20,100,90,30,40,50,60]
    accsum =itertools.accumulate(vals)
    print("-"*50)
    for i in accsum:
        print(i) # you geta cumulative total.

    print("*"*50)
    acc =itertools.accumulate(vals,max)
    for i in acc:
        print(i) #


    # Use chain to connect sequences
    x = itertools.chain("ABCD","1234",[1,3,4,5])
    print("*"*50)
    print(list(x))
    print(type(list(x)))
    print(len(list(x)))

    # dropwhile and takewhile will return values till a condition is met.
    print(list(itertools.dropwhile(testFunc, vals)))
    # drops values till it first encounters x<40 and then returns everything
    print(list(itertools.takewhile(testFunc, vals)))
    # returns first few values till it first encounters x<40


if __name__ == '__main__':
    main()
