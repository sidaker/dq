import module

'''
$ cd __pycache__/
$ ls
module.cpython-37.pyc

A new subfolder has appeared when you run main.py - can you see it?
Its name is __pycache__.
There is a file named (more or less) module.cpython-xy.pyc where x and y are digits derived from your version of Python
(e.g., they will be 3 and 8 if you use Python 3.8).

pyc - python and compliled
When Python imports a module for the first time, it translates its contents into a somewhat compiled shape.
The file doesn't contain machine code - it's internal Python semi-compiled code,
ready to be executed by Python's interpreter.

When a module is imported, its content is implicitly executed by Python.
It gives the module the chance to initialize some of its internal aspects (e.g., it may assign some variables with useful values).

Note: the initialization takes place only once, when the first import occurs, so the assignments done by the module aren't repeated unnecessarily.
'''
