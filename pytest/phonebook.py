import os

class NewPhonebook():

    def __init__(self) -> None:
        self.numbers = {}
        self.filename = "phonebook.txt"
        self.cache = open(self.filename, "w")

    def addphone(self, name,phonenumber):
        self.numbers[name] = phonenumber

    def lookup(self, name):
        return self.numbers[name]

    def names(self):
        return self.numbers.keys()

    def clear(self):
        self.cache.close()
        os.remove(self.filename)
