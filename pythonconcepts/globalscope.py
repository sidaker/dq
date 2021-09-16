p = 2

print("Initial P:",p)
def lfunc():
    p=3
    print("Local P:",p)

def gfunc():
    global p
    print("Global P:",p)
    p =10



if(__name__ == "__main__"):
    lfunc()
    gfunc()
    print("Final P:",p) # Altered in gfunc()
