li1 = [1,2,3,4]

iteratorobj = iter(li1)
print(iteratorobj)
print(next(iteratorobj))
print(next(iteratorobj))
print(next(iteratorobj))
print(next(iteratorobj))
try:
    print(next(iteratorobj))
except StopIteration:
    print("No more items")


li2 = ['1',2,3,4]
# TypeError: 'list' object is not an iterator
# print(next(li2))

### Create an iterable by creating/instantiating a list or doct or tuple
### ### Create an iterable by creating generating objects by using generator functions or expresions

def ite_oceans():
    yield 'Pacific'
    yield 'Atlantic'
    yield 'Indian'
    yield 'Arctic'
    yield 'Southern'


print(next(ite_oceans()))
print(next(ite_oceans()))

iterobj2 = iter(ite_oceans())
print(iterobj2)
print(next(iterobj2))
print(next(iterobj2))
print(next(iterobj2))

iterobj3 = iter(ite_oceans())
print(" ".join(iterobj3))
