name1 = 'Advik'
name2 = 'Likhi'
print(f'Hello Doctor {name1} and {name2}. Dr {name1} is an Cardiologist')
print(f'See how " Double Quotes are represented"')

bytestr = b'these are bytes'
str1=  bytestr.decode()
# Convert bytes to strings using decode.
print(f'{str1} : is of type {type(str1)}')
print(f'{bytestr} : is of type {type(bytestr)}')

# we can also use .format
print("Hello Dr.{} and Dr {}".format(name1,name2))
#print("Dr {} your monthly salary is £{%2f}".format(name1,15000.25))
print("str1" "str2") # See how they are concatenated.
print("z".join("str2")) # See how z is joined with each string element.
print(";".join(["hello","Advik","Babu"]))
# strings are a sequence of unicode charatcers in python and immutable.

# use escape sequence
print(f'Hello this a \' in a string \xe5 ')

arr,_,dep = "London:Edinburg".partition(":")
print(f'from {arr} to {dep}')
print('starting at {pos[0]} reaching {pos[1]} and price {pos[2]:.2f}'.format(pos=("09:00","10:00",123.4567)))
