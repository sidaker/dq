# list reversed vs list.reverse()
# list sorted by list.sort()

list1 = [2,4,5,1,7,8]
list2 = sorted(list1) # Sorts list in place

print(list1) # Original list remains unaltered.
print(list2) # the new list is sorted

list1 = [2,4,5,1,7,8]
print(list1.sort()) # Returns None but sorts the list in place.
print(list1) # Sorts list in place

'''
The primary difference between the list sort() function and the sorted() function is that
the sort() function will modify the list it is called on. Sorts in place.
The sorted() function will create a new list containing a sorted version of the list it is given.
Which one modified the list in place? Answer: sort()
'''

vegetables = ['squash', 'pea', 'carrot', 'potato']

new_list = sorted(vegetables)

# new_list = ['carrot', 'pea', 'potato', 'squash']
print(new_list)

# vegetables = ['squash', 'pea', 'carrot', 'potato']
print(vegetables) # list is not modified in place.

vegetables.sort()

# vegetables = ['carrot', 'pea', 'potato', 'squash']
print(vegetables)
