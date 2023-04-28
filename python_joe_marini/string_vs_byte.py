'''

Question can you comibine bytes and Strings?

No. They are different.
Strings are a sequence of ASCII characters(UTF-8)

You need to decode bytes to strings
or encode strings to bytes before joining

'''


b = b'ABCD'
s = 'This is a string'

try:
    ## fails
    print(b+s)
except TypeError:
    print("error")


print(b.decode('utf-8') +  s)
print(s.encode() +  b)
print(s.encode('utf-8') +  b)

## you can encode the text to UTF-8
print(s.encode('utf-32'))


print(bool(set()))
print(bool(range(0)))