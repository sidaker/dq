class ExampleClass:
    def __init__(self, val = 1):
        self.first = val

    def set_second(self, val):
        self.second = val


example_object_1 = ExampleClass()
example_object_2 = ExampleClass(2)

example_object_2.set_second(3)

example_object_3 = ExampleClass(4)
example_object_3.third = 5
'''
example_object_3 has been enriched with a property named third just on the fly, outside the class's code
- this is possible and fully permissible.
'''

print(example_object_1.__dict__)
print(example_object_2.__dict__)
print(example_object_3.__dict__)

'''
Python objects, when created, are gifted with a small set of predefined properties and methods.
Each object has got them, whether you want them or not. One of them is a variable named __dict__ (it's a dictionary).
The variable contains the names and values of all the properties (variables) the object is currently carrying.
'''
