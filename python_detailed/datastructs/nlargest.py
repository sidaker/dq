import heapq
list1 = [22, 39, 2,6,7,8,33,44,30]

print(heapq.nlargest(3, list1))
print(heapq.nsmallest(3, list1))

list2 = [20, 39, 2,6,7,8,33,44,30]
heap = list(list2)
heapq.heapify(heap)
heapq.heappop(heap)
print(heap)

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
heap = list(nums)
heapq.heapify(heap)
heapq.heappop(heap)
heapq.heappop(heap)
print(heap)


portfolio = [
       {'name': 'IBM', 'shares': 100, 'price': 91.1},
       {'name': 'AAPL', 'shares': 50, 'price': 543.22},
       {'name': 'FB', 'shares': 200, 'price': 21.09},
       {'name': 'HPQ', 'shares': 35, 'price': 31.75},
       {'name': 'YHOO', 'shares': 45, 'price': 16.35},
       {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
print(cheap)
print(expensive)
