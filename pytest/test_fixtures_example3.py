# /Users/sbommireddy/Documents/python/assignments/dq/pytest
# python -m pytest
# python -m pytest
# pytest --fixtures .
# https://github.com/emilybache/Phone-Numbers-Kata
# https://github.com/emilybache/pytest-approvaltests
# pip install pytest-html
# python -m pytest --html=report.html
# python -m doctest test_fixtures_example3.py -v
# python -m pytest --doctest-modules

import pytest
#import doctest
from newphonebook import NewPhonebook1


@pytest.fixture
def pb(tmpdir):
    '''
    Fixture created by Sid Bommireddy for creating a phonebook resource
    '''
    # For each test case that requires the phonebook resource,
    # once the resource is handed over phonebook.txt is cleared
    # pytest will supply tmpdir at run time, clears down temporary directory post each test case.
    # tmpdir is a built-in test fixture.
    # pb is a user defined test fixture using the built-in test fixture tmpdir.
    return NewPhonebook1(tmpdir)


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


def small_straight(dice):
    """
    Score the given roll in the 'small straight yatzy'

    >>> small_straight([1,2,3,4,5])
    15
    >>> small_straight([1,2,3,2,5])
    0
    """

    if dice == [1,2,3,4,5]:
        return sum(dice)
    return 0
