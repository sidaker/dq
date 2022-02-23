'''
zip vs zip_longest
'''


list1 = ['A','B','C']
list2 = [1,2]

for l,n in zip(list1,list2):
    print(l)
    print(n)

print("*******")
from itertools import zip_longest
for l,n in zip_longest(list1,list2):
    print(l)
