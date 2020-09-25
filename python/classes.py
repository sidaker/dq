'''
The self is used to represent the instance of the class.
With this keyword, you can access the attributes and methods of the class in python.
It binds the attributes with the given arguments.

The self parameter is a reference to the current instance of the class,
and is used to access variables that belongs to the class.

It does not have to be named self , you can call it whatever you like,
but it has to be the first parameter of any function in the class:

'''
class myClass():

    def __init__(self, name):
        self.name = name

    def method1(self):
        print("my parent class method of instance ",self.name)


    def method2(self, string1):
        print("Printing " + string1)

class childClass(myClass):

    def method1(self):
        myClass.method1(self) # why self?
        print("my child class method")

    def method2(self, string2):
        print("Printing " + string2)

if __name__ == '__main__':
    c = myClass("Random")
    c.method1()
    c.method2("Hello")

    print("*"*50)
    child = childClass("gotit")
    child.method1()
    child.method2("second")
