from operator import itemgetter, attrgetter
rows = [
        {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
        {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
        {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
        {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]


## sort dictionary
##print(sorted(rows)) # TypeError: '<' not supported between instances of 'dict' and 'dict'
print(sorted(rows,key=itemgetter('fname')))

class User:
    def __init__(self,uid):
        self.uid= uid

    def __repr__(self):
        return str(f"User{self.uid}")

u1 = User(111)
u2 = User(22)
u3 = User(3)
u4 = User(5)


users = [u1,u2,u3,u4]
print(sorted(users,key=attrgetter('uid')))
print(min(users,key=attrgetter('uid')))
print(max(users,key=attrgetter('uid')))
