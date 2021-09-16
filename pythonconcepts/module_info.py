# python 3
import os
import re
import sys
import pprint

# prints a list of existing modules
print( help('modules'))
# pretty print loaded modules
pprint.pprint(sys.modules)

# pretty print module search paths
pprint.pprint(sys.path)


# print the module's online manual
print(help(os))

# print all names exported by the module
print(dir(re))

# example of using a function
# get current dir
print(os.getcwd())

print(dir())

print(dir("__main__"))
