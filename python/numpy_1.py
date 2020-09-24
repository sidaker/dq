import numpy as np


a = np.array([0, 0.5, 1.0, 1.5, 2.0])
print('*'*50)
print(a)
print(a.sum())
print(a.std())
#print(a.csum())

b = np.arange(2, 20, 2)
print('*'*50)
print(b)

c = np.arange(8, dtype=np.float)
print('*'*50)
print(c)

d = np.zeros((2, 3), dtype='i', order='C')
print('*'*50)
print(d)
