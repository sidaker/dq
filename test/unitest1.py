'''
JUnit is a popular unit testing framework in Java.
Python's Unittest framework is inspired from it.
Tests written with the help of unittest must be writteninside of classes
- Java, unlike Python, does not allow purely procedural code and unittest reflects this.
'''

'''
The unittest module provides
a runner to execute our tests,
means of grouping tests into logical units,
and the concept of setup
and teardown to provide a consistent environment for our tests.
calling their setUp method first if provided (functions defined inside a class are called methods), calling each
of the methods whose name start with test, finally calling a tearDown method if provided.
'''


import unittest

#  A TestCase is a class that inherits from unittest.TestCase.
#  In Python
#  we create inheritance by passing a list of parent classes in parentheses after the name of our class.
class ObviousTest(unittest.TestCase):
    # setUp is called first if defined.
    # The setUp method allows us to prepare the environment in which our tests will be run
    def setUp(self):
        self.num = 1

    # names should start with test_
    def test_math(self):
        self.assertEqual(self.num, 0)

    def test_divides_by_zero(self):
        self.assertRaises(ZeroDivisionError, lambda : 1/0)

'''
The unittest test runner outputs a dot (.) for each sucessful test, an "F" for any tests
that do not pass, and an "E" for tests that failed to run due to errors in the test or in code it tested.
'''
if __name__ == '__main__':
    unittest.main()
