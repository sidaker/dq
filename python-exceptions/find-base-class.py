'''

 inspect.getmro(cls) works for both new and old style classes and returns the
 same as NewClass.mro():
 a list of the class and all its ancestor classes, in the order used for method resolution.
'''
import inspect

class A(object):
    pass

class B(A):
    pass



print(inspect.getmro(B))
