a=2
b=3

print(a+b)
print(a.__add__(b))

'''
the author of a class may provide a definition using a technique
known as operator overloading.
the + operator is overloaded by implementing a method named __add__
'''

print(a*b)
print(a.__mul__(b))

c=-3
print(abs(c))
print(c.__abs__())

print(3 * 'loveme')

'''
 Python's polymorphism
'''

print(1+2)
print("Sid" + " B")
