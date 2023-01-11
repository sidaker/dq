li = [1,2,3,4,5,6,7]

print(li[::-3])
li.pop() ## pop the element at the end of the list
print(li)
li.append(8) ## appends to the end of the list.
print(li)


'''
Keep last N items.
List's pop and append are not exact a queue operation FIFO.
List is rather a LIFO i.e. a Stack.
So to answer this we can use the collections.deque
'''
from collections import deque

qlist = deque(maxlen = 3)
qlist.append(3)
qlist.append(5)
qlist.append(7)
print(qlist)
qlist.append(9)
print(qlist)

qlist2 = deque(li, maxlen = 3)
qlist2.append(99)
print(qlist2)

'''
append():- This function is used to insert the value in its argument to the right end of the deque.
appendleft():- This function is used to insert the value in its argument to the left end of the deque.
pop():- This function is used to delete an argument from the right end of the deque.
popleft():- This function is used to delete an argument from the left end of the deque.

index(ele, beg, end):- This function returns the first index of the value mentioned in arguments, starting searching from beg till end index.
insert(i, a) :- This function inserts the value mentioned in arguments(a) at index(i) specified in arguments.
remove():- This function removes the first occurrence of value mentioned in arguments.
count():- This function counts the number of occurrences of value mentioned in arguments.
'''
qlist2.appendleft(100)
print(qlist2)
print(qlist2.count(2))
print(qlist2.count(100))
