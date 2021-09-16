class A:
    val = 1

class B(A):
    val = 2

class C(B):
    #val = 3
    pass


o =  C()
print(o)
print(o.val) # Returns 2. How?. v is a class variable.
