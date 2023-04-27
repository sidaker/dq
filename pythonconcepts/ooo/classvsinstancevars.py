class User:
    ## static var
    active_users = []

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def activate(self):
        if self not in self.__class__.active_users:
            # add to list
            self.__class__.active_users.append(self)

    def deactivate(self):
        if self in self.__class__.active_users:
            # add to list
            self.__class__.active_users.remove(self)

    def is_active(self):
        return self in self.__class__.active_users

me = User("Sid", "Sid@example.com")
me.activate()
print(me.is_active())
me.deactivate()
print(me.is_active())
print(me.__dict__)
print(User.__dict__)
print(dir(me))
print(isinstance(me, User))
print(isinstance(me, object))