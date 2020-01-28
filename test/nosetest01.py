# python3 -m nose -v nosetest01.py
# python3 -m nose -vs nosetest01.py
# no need of any classes.
from nose.tools import with_setup

def test_case99():
    #uses python's built in assert function.
    #unittest has assert methods
    assert 'aaa'.upper() == 'AAA'

'''
As you can see in the output, setup_function() and teardown_function() run before and after test_case03(), respectively. unittest does not have any provision for the fixtures at the test function level. Actually, unittest does not support the concept of standalone test functions, as everything has to be extended from the TestCase class and a function cannot be extended.
'''

def setUpModule():
    """called once, before anything else in this module"""
    print("\nIn setUpModule()...")

def tearDownModule():
    print("\nIn tearDownModule()...")
def setup_function():
    """setup_function(): use it with @with_setup() decorator"""
    print("\nsetup_function()...")
def teardown_function():
    """teardown_function(): use it with @with_setup() decorator"""
    print("\nteardown_function()...")
def test_case01():
    print("In test_case01()...")
def test_case02():
    print("In test_case02()...")

@with_setup(setup_function, teardown_function)
def test_case03():
    print("In test_case03()...")
