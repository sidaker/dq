# pytest -v
# pytest -v -s
# pytest -v -s test_file.py


class TestClass:
    @classmethod
    def setup_class(cls):
        print("Setup Test Class")

    @classmethod
    def Teardown_class(cls):
        print("Teardown Test Class")


    def setup_method(self, method):
        if method == self.test1:
            print("\n Setting up test1")
        if method == self.test2:
            print("\n Setting up test2")
        else:
            print("\n Setting up unknown test")

    def test_me1(self):
        assert True

    def test_me2(self):
        assert True

    def test1(self):
        print("Executing test1")
        assert True


    def test2(self):
        print("Executing test2")
        assert True
