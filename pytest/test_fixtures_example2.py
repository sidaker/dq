# /Users/sbommireddy/Documents/python/assignments/dq/pytest
# python -m pytest
# python -m pytest
# pytest --fixtures .
import pytest
from phonebook import NewPhonebook


@pytest.fixture
def pb():
    '''
    Fixture created by Sid Bommireddy for creating a phonebook resource
    '''
    # Replaced return with yield
    # For each test case that requires the phonebook resource,
    # once the resource is handed over phonebook.txt is cleared
    # pytest can supply tmpdir at run time as an alternative.
    phonebook = NewPhonebook()
    yield phonebook
    # Below tear down runs after each test case.
    phonebook.clear()

# Test Case 1
def test_phonebook_lookup(pb):
    #pb = Phonebook()
    pb.addphone("Sid","0756")
    assert "0756" == pb.lookup("Sid")

# Test Case 2
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
