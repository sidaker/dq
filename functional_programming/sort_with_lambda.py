chessplayers = ['V Anand','Advik Bommireddy','M Tal','M Carlsen','A Giri']
print(sorted(chessplayers)) # sorts by First name.
# use  a lambda to pass last name as ke for sorted.
print(sorted(chessplayers, key= lambda name: name.split()[-1]))


## Create a callable function using lambda.
lname = lambda name: name.split()[-1]
print(lname)
print(lname("Sid Bommireddy"))

# lambdas, functions, classes, ,methods are all callable.
print(callable(lname))
print(callable(list))
print(callable(list.append))

# strings are not callable
print(callable("hello"))
