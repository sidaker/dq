def outerfunc(msg):
    def innerfunc(name):
        print(f'{msg}  {name}')
    return innerfunc


myf1 = outerfunc('hi')
myf2 = outerfunc('bye')

myf1('sid')
myf1('advik')
myf2('Sid')



