def decorated_by(func):
    func.__doc__ += '\nDecorated by decorated_by.'
    return func

def also_decorated_by(func):
    func.__doc__ += '\nWrapped by decorated_by.'
    return func

def add(x, y):
    """Return the sum of x and y."""
    return x + y

def add(x, y):
    """Return the sum of x and y."""
    return x + y
add = decorated_by(add)

print(help(add))

@decorated_by
def sub(x, y):
    """Return the difference of x and y."""
    return x + y

print(help(sub))

@also_decorated_by
@decorated_by
def sub(x, y):
    """Return the difference of x and y."""
    return x + y

print(help(sub))


## https://thispointer.com/pandas-select-dataframe-columns-containing-string/
