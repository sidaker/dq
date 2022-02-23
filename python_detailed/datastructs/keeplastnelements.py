'''
always pop the first element and append the last ement if length of the list > 3
'''
from collections import deque
## https://www.geeksforgeeks.org/deque-in-python/

list1  = [1,2,3]
list1.pop(0)
list1.append(4)
print(list1)

'''
Using deque(maxlen=N) creates a fixed-sized queue
'''
list2 = deque(maxlen=4)
for i in range(8):
    list2.append(i)
print(list2) ## deque([4, 5, 6, 7], maxlen=4)

# Declaring deque
queue = deque(['name','age','DOB'])
print(queue)
print(type(queue)) ## <class 'collections.deque'>
queue.popleft()
queue.append("Welcome new") ## removes the first occurrence of value mentioned
queue.remove('DOB')
print(queue)

'''
do a simple text match
and provide the line and the last N lines.
'''
import os
dirname = os.path.dirname(__file__)
print(dirname)
filename = os.path.join(dirname, 'unpack_sequences.py')

def mysearch(lines,patt,history=3):
    prev_lines =deque(maxlen=history)
    for line in lines:
        if patt in line:
            yield line, prev_lines
        prev_lines.append(line)    


if __name__ == '__main__':
    #dq/python_detailed/datastructs/unpack_sequences.py
    with open(filename) as f:
        print(type(f)) ## <class '_io.TextIOWrapper'>
        for line, prevlines in mysearch(f,'ValueError',3):
            print(line, prevlines)
