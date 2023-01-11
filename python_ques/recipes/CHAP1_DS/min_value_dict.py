prices = {
       'ACME': 45.23,
       'AAPL': 612.78,
       'IBM': 205.55,
       'HPQ': 37.20,
       'FB': 10.75
}

print(min(zip(prices.values(), prices.keys())))
print(max(zip(prices.values(), prices.keys())))
print(min(prices)) ## We dont want min key value which is based on alphbet order
print(sorted(zip(prices.values(), prices.keys())))
