import unittest
import inspect

# inspect.stack()[0][3] method prints the name of the current test method.
# It’s useful for debugging when you want to know the order that the methods are executed in the test class.

# Why does test_case01 get executed before test_case02?
# Note that the test methods ran in alphabetical order, irrespective of the order of the test methods in the code.

class TestClass02(unittest.TestCase):
        def test_case02(self):
                print("\nRunning Test Method : " + inspect.stack()[0][3])
        def test_case01(self):
                print("\nRunning Test Method : " + inspect.stack()[0][3])
if __name__ == '__main__':
        unittest.main(verbosity=2)
