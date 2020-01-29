import sys
import unittest

# python -m unittest skippingtests.py -v

'''
Tests can be
    - skipped
    - failed due to an assertion
    - Error due to an Exception
In this case we are not failing fast.
'''

class TestClass13(unittest.TestCase):

    @unittest.skip("demonstrating unconditional skipping")
    def test_case01(self):
        print("This test will always be skipped")
        self.fail("FATAL")

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_case02(self):
        # Windows specific testing code
        print("Only executes in Windows Environment")

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux")
    def test_case03(self):
        # Linux specific testing code
        print("Only executes in Linux Environment")

    def test_case05(self):
        """This is a test method.We are intentionally failing it"""
        print(self.id())
        self.fail()

    def test_case06(self):
        """This is a test method.We are raising an exception to create an error"""
        print(self.id())
        raise Exception

    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires darwin")
    def test_case04(self):
        # Darwin specific testing code
        print("Only executes in Darwin Environment")
