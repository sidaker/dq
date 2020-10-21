listA = ["Outer-", "Frost-", "Sun-"]
listB = ['Space', 'bite', 'rise']
print(listA)
# Given lists
print("Given list A: ", listA)
print("Given list B: ",listB)
# Use zip
res = [i + j for i, j in zip(listA, listB)]
# Result
print("The concatenated lists: ",res)

print(zip(listA, listB))

# Use map
# Double all numbers using map and lambda

numbers = (1, 2, 3, 4)
result = map(lambda x: x + x, numbers)
print(list(result))

# Add two lists using map and lambda

numbers1 = [1, 2, 3]
numbers2 = [4, 5, 6]

result = map(lambda x, y: x + y, numbers1, numbers2)
print(list(result))



listb = [{'Values': ['2020-08-04/180019']},{'Values': ['2020-09-25/09:10:23.598878-consolidated']} ]
print(len(listb))

x = [[]]
for idx,val in enumerate(listb):
     x[0].append(val)


print(x)
print(len(x))


numbers = [1, 2, 3, 4]

def less_than_three(number):
	return number < 3

an_iterator = filter(less_than_three, numbers)
# select only numbers less than `3`

filtered_numbers = list(an_iterator)

print(filtered_numbers)

# Add 2 lists
print(numbers1 + numbers2)
if 1 in numbers1:
    print('1 is Present')

if 11 in numbers1:
    print('11 is Present')

# In a list of lists edit an element at a index inside each list.
myList = [1,2,3,4]
A = [myList]*3
myList[2]=45
print(A)
print(myList)
# myList.reverse() it does an in place reversal of the list and returns None.
myList.reverse()
print(myList)

# you can convert a dictionary to a list of tuples
print(list({1:'Hello',2:2,3:3}))
a= {1:"Ok",2:"Google",3:3}
print(list(a.items()))
