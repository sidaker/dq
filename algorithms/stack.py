# implement a stack using a python list

# push - add an element to a stack
# pop - remove an element from a stack
# size - return size of stack
# initialize and create an empty stack
# isEmpty - Check if empty stack
# check -  Check if an element exists. Not a stack property.
# peek - return top element but does not remove it.

class Stack:

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)


    def push(self, elem):
        self.items.append(elem)

    def pop(self):
        return self.items.pop()

    def check(self, elem):
        return elem in self.items

    def peek(self):
        return self.items[len(self.items)-1]

    def __str__(self):
        return str(self.items)

    def isEmpty():
        return self.items == []


if __name__ == '__main__':
    s1 =  Stack()
    # s1.pop()  # IndexError: pop from empty list
    print(s1)
    s1.push(2)
    s1.push(3)
    s1.push(9)
    print(s1.peek())
    print(s1)
    print(s1.size())
    s1.pop()
    print(s1)
    print(s1.peek())
