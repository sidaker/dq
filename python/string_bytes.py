b = b'46'
s = 'ABC'

b1 = bytes([0x41,0x42,0x44])
print(b1)

# TypeError: can only concatenate str (not "bytes") to str
#print(s+b)

# Convert byte to String. use decode for that.
c= b.decode('utf-8') + s
print(c)
print(b1.decode('utf-8') + s)


# Convert string to bytes. use encode for that.
e = s.encode()+ b + b1
print(e)
