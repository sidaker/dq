'''
Stacks LIFO. eg. backtracking on your browser.
Queues FIFO. eg. order processing.

Using a regular queue in python.
Removing items from front of a queue needs a BIG O of Linear time complexity.
Use deque instead.
'''

from collections import deque
# deque optimised for adding and removing elements from both sides of rthe queue.

queue = deque()
queue.append(1)
queue.append(2)
queue.append(3)
queue.append(4)
print(queue)
print(type(queue))
# remove an item from the front of the queue. FIFO.
queue.popleft()
print(queue)
queue.pop()
print(queue)
