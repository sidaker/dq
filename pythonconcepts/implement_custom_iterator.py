# Create a Class myiter
# Implement next method
# Class to raise an StopIteration  exception when no further elements

#

class myter:
    def __init__(self,start=0):
        self.num = start

    def __next__(self):
        num = self.num
        self.num += 1
        return num


    def __iter__(self):
        return self


if __name__ == '__main__':
    x = myter(3)
    for i in x:
        print(i)
        if(i>5):
            break
    print("*"*50)
    y =  myter()
    print(y.__next__())
    print(y.__next__())
    print(y.__next__())
    assert y.__next__() == 3
    print(next(y))

    
