x = "outer variable"
y = "global variable"

def foo():
    # UnboundLocalError: local variable 'x' referenced before assignment
    #x = x * 2
    global y
    print(f'y inside is {y}')
    y = "update global"
    print(f'x inside is {x}')


foo()
print(f'y outside is {y}')
print(f'x outside is {x}')
