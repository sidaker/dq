# /Users/sbommireddy/Documents/python/assignments/dq/pytest
# python -m pytest
# python -m pytest
# pytest --fixtures .
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



@pytest.fixture
def pb():
    '''
    Fixture created by Sid Bommireddy for creating a phonebook resource
    '''
    return Phonebook()

def test_phonebook_lookup(pb):
    #pb = Phonebook()
    pb.addphone("Sid","0756")
    assert "0756" == pb.lookup("Sid")

def test_phonebook_contains(pb):
    #pb = Phonebook()
    pb.addphone("Sid","0756")
    pb.addphone("Lik","0776")
    print(type(pb.names()))
    assert pb.names() == {"Sid","Lik"}
    #assert "Advik" in pb.names()
    assert "Lik" in pb.names()
    with pytest.raises(KeyError):
        pb.lookup("Ash")

    with pytest.raises(KeyError):
        pb.lookup("Roc")
