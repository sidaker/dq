## Linked list
'''
HEAD
Node
Tail
'''

class Node(object):
    def __init__(self,val):
        self.val = val
        self.next = None

    def get_data(self):
        return self.val

    def set_data(self, val):
        self.val = val

    def get_next(self):
        return self.next

    def set_next(self, next):
        self.next = next


class LinkedList(object):
    def __init__(self,head=None):
        self.head = head
        self.count = 0 # Keeps track of number of nodes in the list.

    def get_count(self):
        return self.count

    def insert(self, data):
        '''
        Insert a new Node at the beginning of the list.
        '''
        newnode = Node(data)
        newnode.set_next(self.head) # current head becomes next.
        self.head = newnode # head points to new node.
        self.count += 1

    def find(self, val):
        '''
        Find first item with a give value.
        Start from head and traverse the list.
        '''
        item =  self.head
        while(item != None):
            if(item.get_data() == val):
                return item
            else:
                item =  item.get_next()
            # What happens if item not found
        return None


    def deletaAt(self, idx):
        '''
        delete a node at a given index.
        if you delete the HEAD node, you have to set the new head node.
        '''

        if(idx > self.count-1):
            return None
        elif(idx == 0):
            self.head = self.head.get_next()
        else:
            tempIdx = 0
            node = self.head
            while (tempIdx  < idx -1):
                node = node.get_next()
                tempIdx += 1
            # now you are at the node index immediately before the one we delete.
            # Whole idea is to fix the next pointer of the one before the node we are deleting.
            node.set_next(node.get_next().get_next())
            self.count -= 1


    def dump_list(self):
        tempnode = self.head
        while (tempnode != None):
            print("Node: ", tempnode.get_data())
            tempnode = tempnode.get_next()


if __name__ == '__main__':
    itemlist = LinkedList()
    itemlist.insert(38)
    itemlist.insert(48)
    itemlist.insert(13)
    itemlist.insert(15)
    itemlist.dump_list()
    print("*"*50)
    itemlist.deletaAt(3)
    itemlist.dump_list()
    itemlist.deletaAt(3)

    print("Item Count:",itemlist.get_count())
    print("Finding an item:",itemlist.find(13))
    print("Finding an item:",itemlist.find(48))
    print("Finding an item:",itemlist.find(24))
