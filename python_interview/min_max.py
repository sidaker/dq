'''
Write two Python functions to find the minimum number in a list.
The first function should compare each number to every other number on the list.
𝑂(𝑛2). The second function should be linear 𝑂(𝑛).
'''

import time

def minn(listn):
    # Big(0) of n
    min = listn[0]
    for idx in range(len(listn)-1):
        if min > listn[idx+1]:
            min = listn[idx+1]
    return min

def minn2(listn):
    # Big(0) of n2
    for idx in listn:
        pass

if __name__ == '__main__':
    print(minn([2,4,5,1,8,9]))
    #minn2([2,4,5,1,8,9])
    print(minn(list(range(1000,10,-1))))
    #minn2(list(range(1000,0,-1)))
