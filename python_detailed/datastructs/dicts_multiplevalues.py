from collections import defaultdict
from collections import OrderedDict
d = defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)
print(d)# every value is a list.


d = defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['b'].add(4)
print(d)# every value is a list.

a={
'x' : 1,
'y' : 2,
'z' : 3 }

b={
'w' : 10,
'x' : 11,
'y' : 2 }

# Find keys in common
print(a.keys() & b.keys()) # { 'x', 'y' }
# Find keys in a that are not in b
print(a.keys() - b.keys() )# { 'z' }
# Find (key,value) pairs in common
a.items() & b.items() # { ('y', 2) }


# Make a new dictionary with certain keys removed
c = {key:a[key] for key in a.keys() - {'z', 'w'}}
print(c)
# c is {'x': 1, 'y': 2}
