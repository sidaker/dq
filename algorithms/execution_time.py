import time
'''
In the time module there is a function called time that will return the
current system clock time in seconds since some arbitrary starting point.
By calling this function twice, at the beginning and at the end, and then
computing the difference, we can get an exact number of seconds
(fractions in most cases) for execution.
https://runestone.academy/runestone/books/published/pythonds/AlgorithmAnalysis/BigONotation.html

'''
start = time.time()
time.sleep(1)
end = time.time()
print(end-start)
