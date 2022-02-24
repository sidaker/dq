prices = {
       'ACME': 45.23,
       'AAPL': 612.78,
       'IBM': 205.55,
       'HPQ': 37.20,
       'FB': 10.75
}


min_price = min(zip(prices.values(),prices.keys()))
print(min_price)
print(min(prices, key=lambda k: prices[k])) # Returns 'FB'

ordered_prices = sorted(zip(prices.values(),prices.keys()))
print(ordered_prices)


prices_and_names = zip(prices.values(), prices.keys())
# zip() creates an iterator that can only be consumed once.
print(min(prices_and_names)) # OK
try:
    print(max(prices_and_names)) # ValueError: max() arg is an empty sequence
except ValueError:
    print("Error")
