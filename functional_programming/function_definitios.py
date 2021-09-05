import socket

def resolve(host):
    return socket.gethostbyname(host)

print(resolve)
print(resolve("www.google.co.uk"))
# __call__ is invoked on objects when they are called like functions.
print(resolve.__call__("www.google.co.uk"))


from timeit import timeit
print(timeit(setup="from __main__ import resolve",
stmt="resolve('google.co.uk')", number=1))
'''
 the timeit function accepts two code snippets as strings,
 one of which is used to perform any set up operations and the other of which
 is the code for which the elapsed time will be reported.
 The function also accepts a number argument, which is the count of how many
 times the code under test will be run.
 You can see here that the DNS lookup took around 1/100 of a second. 
'''
