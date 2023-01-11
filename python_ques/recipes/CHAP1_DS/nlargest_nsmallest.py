import heapq

li = [1,3,5,7,2,55,32,10]
print(heapq.nlargest(3,li))
print(heapq.nsmallest(3,li))
print(min(li), max(li))

portfolio = [
       {'name': 'IBM', 'shares': 100, 'price': 91.1},
       {'name': 'AAPL', 'shares': 50, 'price': 543.22},
       {'name': 'FB', 'shares': 200, 'price': 21.09},
       {'name': 'HPQ', 'shares': 35, 'price': 31.75},
       {'name': 'YHOO', 'shares': 45, 'price': 16.35},
       {'name': 'ACME', 'shares': 75, 'price': 115.65}
]

## TypeError: '<' not supported between instances of 'dict' and 'dict'
print(heapq.nlargest(3,portfolio, key=lambda x:x['price']))


nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
heap = list(nums)
print(type(heap))
heapq.heapify(heap)
print(heap)
