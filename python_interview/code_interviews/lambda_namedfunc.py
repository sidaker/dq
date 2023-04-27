def sq(n):
    return n*n

print(sq(2))

lambda_var = lambda x: x*x  # assign lambda func to a variable

print(lambda_var(2))


assert sq(4) == lambda_var(4)

'''
Where you use lambda functions?

In Functional programming where you use function as an argument.
'''