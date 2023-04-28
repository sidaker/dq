'''
example of non idempotent functions
'''


def add10(num):
    return num + 10


print(add10(10))
print(add10(add10(10)))  ## result changes on repeated execution.

print(abs(-10))
print(abs(abs(-10)))   ## result remains on repeated execution.

# typical idempotent methods - http methods - GET, PUT
## POST is not an idempotent method.