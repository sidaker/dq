s1 = ";"

print(s1.join(["Hello", "World"]))
print("My Sir,Likhi".partition(','))

departure,_,arrival = "London:Edinburgh".partition(':')
print(arrival)

print("{} north {} east".format(59.7, 10.4))
print("{0} north {1} east and {0} north".format(59.7, 10.4))

northling=40.4
eastling=34.4
print(f'{northling} N and {eastling} East')

r5 = range(5)
print(r5)

for i in range(1,100,25):
    print(i)

# Copying a list
list1 = [1,2,3,4]
list2 = list1
# Shallow copy
list3 = list1[:]
list4 = list1.copy()
list4 = list(list1)
print(f'id of list1 is {id(list1)} \nid of list2 is {id(list2)}')
print(f'id of list3 is {id(list3)} and it is different to the other 3 due to list copy')

# Even though copied in shallow copy individual elements still refer to same object
print(list1[0] is list3[0])
# For deep copies refer to the copy module in standard library.

print(list1.index(2))
print(2 in list1)

hl = "I dont know. There is so much to learn. I love machine learning".split()
print(hl)
hl.reverse()
print(hl)
hl.sort(key=len)
print(hl)

'''
Difference between
sort and sorted
reverse and reversed
For out‑of‑place equivalents of the reverse and sort list methods, we can use the reversed and sorted built‑in functions. These return a reversed iterator and a newly sorted list, respectively. For example, calling sorted on the list 4, 9, 2, 1 results in an entirely new list with the correctly sorted elements. Calling reversed on a list doesn't give us a new list. Rather, it gives us an object of the type list_reverseiterator. We can pass this iterator to the list constructor to create an actual list. These functions have the advantage that they'll work on any finite, iterable source object.
'''
