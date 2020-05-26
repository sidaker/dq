import socket

def func(host):
    return socket.gethostbyname(host)


# Prints ip address of google.co.uk
print(func("google.co.uk"))

#path = 'C:\Users\Sid\Bucket'
rawpath = r'C:\Users\Sid\Bucket'
print(rawpath)

'''
Strings, Tuples are immutable
Dictionaries and Lists are mutable
Default source encoding in Python is utf-8.
str is unicode
'''

'''
Strings vs bytes
String are sequences of unicode code points.
Bytes are sequences of bytes.
You encode into bytes and decode from bytes.
'''

esp = 'îne klâwen durh die wolken sint geslagen'
data = esp.encode('utf8')
print(type(data))
print(data)

espaniol = data.decode('utf-8')
print(espaniol)
'''
Reverse that by using decode method of bytes object
'''

'''
files and network resources like
http responses are trasnmitted as byte streams.
'''
