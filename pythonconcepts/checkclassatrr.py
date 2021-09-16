class ExampleClass:
    def __init__(self, val):
        self.__venomous = 1
        if val % 2 != 0:
            self.a = 1
        else:
            self.b = 1


example_object = ExampleClass(1)
print(example_object.__dict__)
print(example_object.a)

if hasattr(example_object, 'b'):
    print(example_object.b)

# negating private property ignoring the fact that the property is private. How will you do this?
example_object._ExampleClass__venomous = not example_object._ExampleClass__venomous
print(example_object.__dict__)
