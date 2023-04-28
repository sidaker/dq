def outerfunc():
    message = 'Hi'

    def inner_func():
        print(message)

    return inner_func()

def outerfunc2(msg):
    message = msg

    def inner_func():
        print(message)

    return inner_func()

def outerfunc3(msg):
    message = msg

    def inner_func():
        print(message)

    return inner_func

outerfunc()

outerfunc2("ok")

my_func = outerfunc3("closure")
print(my_func)
print(my_func.__name__)
print(my_func())
my_func()
my_func()
