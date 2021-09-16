# Python program to demonstrate
# infinite iterators

import itertools

# for in loop
for i in itertools.count(5, 5):
	if i == 35:
		break
	else:
		print(i, end =" ")

print('**********')
count = 0

# for in loop
for i in itertools.cycle('AB'):
    if count > 7:
        break
    else:
        print(i, end = " ")
        count += 1

print('**********')
l = ['Advik', 'for', 'Chess']

# defining iterator
iterators = itertools.cycle(l)

# for in loop
for i in range(7):

    # Using next function
    print(next(iterators), end = " ")

# using repeat() to repeatedly print number
print ("Printing the numbers repeatedly : ")
print (list(itertools.repeat(25, 4)))

from itertools import product

print("The cartesian product using repeat:")
print(list(product([1, 2], repeat = 2)))
print()

print("The cartesian product of the containers:")
print(list(product(['geeks', 'for', 'geeks'], '2')))
print()

print("The cartesian product of the containers:")
print(list(product('AB', [3, 4])))    
