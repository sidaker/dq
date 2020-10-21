import time
def sumOfN(n):
   theSum = 0
   st1 =  time.time()
   for i in range(1,n+1):
       theSum = theSum + i
   en1 =  time.time()
   #print(en1-st1) # 50 times faster
   return theSum, en1-st1


def sumOfN3(n):
    st1 =  time.time()
    return (n*(n+1))/2,time.time() - st1

if __name__=='__main__':

    print(sumOfN3(1000000000))
    print(sumOfN(1000000000))
    print("-"*50)
    #result
    '''
    5.000000005e+17
    0.00011682510375976562
    500000000500000000
    50.884262800216675
    First, the times recorded above are shorter than any of the previous examples.
    Second, they are very consistent no matter what the value of n.
    It appears that sumOfN3 is hardly impacted by the number of integers being added.
    '''
    for i in range(5):
       print("Sum is %d required %10.7f seconds"%sumOfN3(1000000))

    print("*"*50)
    for i in [1000000,100000000,200000000]:
       print("Sum is %d required %10.7f seconds"%sumOfN3(i))
