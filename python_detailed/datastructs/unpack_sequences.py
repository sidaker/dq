x,y = [1,2]
print(x,y)


try:
    x,y = [1,2,3]
    print(x,y)
except ValueError as e:
    print(e)

## Unpack arbitrary number of arguments
*x,y = [100,200,3]
print(x,y)


x,y,z,*a = [8,9,10]
print(x,y,z,a)

## You can unpack lists, strings, generators, tuples, iterators
x,*y = (1,2,3)
print(x,y)

x,*y = 'myname'
print(x,y)

x,*y = range(5)
print(x,y)
