# /Users/sbommireddy/Documents/python/assignments/dq/pytest
# python -m pytest
import pytest

class Phonebook():

    def __init__(self) -> None:
        self.numbers = {}

    def addphone(self, name,phonenumber):
        self.numbers[name] = phonenumber

    def lookup(self, name):
        return self.numbers[name]


    def names(self):
        return self.numbers.keys()



def test_phonebook_lookup():
    pb = Phonebook()
    pb.addphone("Sid","0756")
    assert "0756" == pb.lookup("Sid")

def test_phonebook_contains():
    pb = Phonebook()
    pb.addphone("Sid","0756")
    pb.addphone("Lik","0776")
    print(type(pb.names()))
    assert pb.names() == {"Sid","Lik"}
    #assert "Advik" in pb.names()
    assert "Lik" in pb.names()
    with pytest.raises(KeyError):
        pb.lookup("Ash")

    with pytest.raises(KeyError):
        pb.lookup("Lik")
