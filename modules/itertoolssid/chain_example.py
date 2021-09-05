from itertools import chain

x = 'adv'
y = 'ik'
z = 'bommired'
zp = 'dy'

a = [1,2,3]
b = [4,5,6]


for i in x,y,z,zp:
    print(i)

for i in a,b:
    print(i)

print("*********")
for i in chain(x,y,z,zp):
    print(i)


for i in chain(a,b):
    print(i)
