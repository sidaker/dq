# convert_to_numeric wrapper function expects a function as an argument
# and returns another function.
def convert_to_numeric(func):
    # define a function within the outer function
    def new_func(x):
        return func(float(x))
    # return the newly defined function
    # functions are first class in python
    # They can be returned like variables.
    return new_func


if __name__ == "__main__":
    #decors
    @convert_to_numeric
    def first_func1(x):
        return x**2

    # The above syntax is equivalent to:
    def first_func(x):
        return x**2
    first_func = convert_to_numeric(first_func)


    assert first_func1('2') == 4
    assert first_func('9') == 81
