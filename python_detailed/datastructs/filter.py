#The easiest way to filter sequence data is often to use a list comprehension.
mylist = [1, 4, -5, 10, -7, 2, 3, -1]

print([n for n in mylist if n >3])


'''
One potential downside of using a list comprehension is that it might produce a large result if the original input
 is large. If this is a concern, you can use generator expressions to produce the filtered values iteratively.
'''

pos = (n for n in mylist if n > 0)
print(pos)
for x in pos:
    print(x)


values = ['1', '2', '-3', '-', '4', 'N/A', '5']

'''
 We have a list of string which are supposed to hold numbers, if there are non numbers filter them out
'''
def filt(val):
    try:
        n = int(val)
        return True
    except:
        return False


print(filter(filt,values))
print(list(filter(filt,values)))

clip_neg = [n if n > 0 else 0 for n in mylist]
print(clip_neg)

addresses = [
        '5412 N CLARK',
        '5148 N CLARK',
        '5800 E 58TH',
        '2122 N CLARK'
        '5645 N RAVENSWOOD',
        '1060 W ADDISON',
        '4801 N BROADWAY',
        '1039 W GRANVILLE',
    ]
counts = [ 0, 3, 10, 4, 1, 7, 6, 1]

from itertools import compress
more5 = [n > 5 for n in counts]
print(more5)
print(list(compress(addresses, more5)))
## filter(), compress() normally returns an iterator. Thus, you need to use list() to turn the results into a list if desired.
