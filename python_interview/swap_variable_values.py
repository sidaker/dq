
'''
Interview Question?
How to swap values associated with two values using Python's unpacking
'''
j = 3
k = 2


j, k = k, j
print("j:", j)
print("k:", k)

'''
When using a simultaneous assignment, all of the expressions are evaluated on the right-hand side
before any of the assignments are made to the left-hand variables.

Without simultaneous assignment, a swap typically requires more delicate use of a temporary variable, such as


'''

temp = j
j = k
k = temp
print("j:", j)
print("k:", k)
