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
