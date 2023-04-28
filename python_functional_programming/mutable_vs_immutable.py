'''

In Python strings are immutable

'''

a = 'Hello'
print('{a} my memory address is {b}'.format(a=a, b=id(a)))

a = 'Well'
print('{a} my memory address is {b}'.format(a=a, b=id(a)))

'''
String object does not support item assignment
'''
try:
    a[0] =  'C'
    print(a)
except NameError:
    print("Variable is not defined")
except TypeError:
    print("String are immutable.Error!!!")
except:
    print("Something else went wrong")

'''
Lists are mutable
'''
lista = [1,2,3,4]
print('{a} my memory address is {b}'.format(a=lista, b=id(lista)))
lista[0] = 99
print('{a} my memory address is {b}'.format(a=lista, b=id(lista)))
