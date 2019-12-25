import unittest

#python3 test_module01.py -v for a more verbose display of execution
#python3 basicunittest.py -v

class TestClass01(unittest.TestCase):
        # class methods test_case01() and test_case02() are test methods, as their names start with test_
        def test_case01(self):
                my_str = "SidAdvik"
                my_int = 999
                # Below are assesrtion methods
                self.assertTrue(isinstance(my_str, str))
                self.assertTrue(isinstance(my_int, int))

        def test_case02(self):
                my_pi = 3.14
                self.assertFalse(isinstance(my_pi, int))

if __name__ == '__main__':
        # unittest.main() is the test runner.
        unittest.main()
