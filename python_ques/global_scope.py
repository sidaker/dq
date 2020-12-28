##  Question. What happens if you don't define a  variable as  global.
##  Scopre can be
##    - LOCAL(inside current function),  Enclosing, GLOBAL, Built-in (LEGB)
##  you bind a name to an object
##  Name resolution to objects is manged by scopes and scoping rules.
# https://www.programiz.com/python-programming/namespace

lcount=0
gcount=0
#print(id(lcount))
#print(id(gcount))

def showcount():
    # lcount += 1 ## UnboundLocalError: local variable 'lcount' referenced before assignment
    print(lcount, ' and ' ,gcount )

def setcount(c):
    global gcount
    #print(id(gcount))
    lcount = c # c is bind to a new name called lcount in the inner most name space
    # a new variable lcount is created in local name space which shadows access to glabal variable with same name
    gcount = c
    print(dir()) # What objects are in local or function name namespace?
    #print(id(lcount))
    #print(id(gcount))



if __name__=='__main__':
    showcount()
    setcount(3)
    showcount()
    print(dir()) # What objects are in global or module name namespace?
