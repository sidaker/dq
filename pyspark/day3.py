# scopetest1.py
# scopetest2.py

# importing modules
import funcstobeimported
from funcstobeimported1 import scopeTest
import sys, keyword
from datetime import *
from time import *
start_timer = time()
# the above imports the functions into the programs own symbol table
funcstobeimported.echo('Sid','Python','Mac')
print(scopeTest(2))

print('Python version:',sys.version)
print('Python Interpreter Location:',sys.executable)

# list of all directories where interpreter looks for module files
for dir in sys.path:
    print(dir)


print('Python Keywords')
for word in keyword.kwlist:
    print(word)

print('Today is:', datetime.today())
print('Current hour is:', getattr(datetime.today(),'hour'))
print('Current month is:', getattr(datetime.today(),'month'))

sleep(2)

end_timer = time()

difference = round(end_timer - start_timer)

print('\nRuntime:', difference,'seconds')
