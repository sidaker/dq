# pytest -v
# pytest -v -s
# pytest -v -s test_file1.py


def setup_function(function):
    if function == test1:
        print("\n Setting up test1")
    elif function == test2:
        print("\n Setting up test2")
    else:
        print("\n Setting up unknown test")


def teardown_function(function):
    if function == test1:
        print("\n Tearing Down test1")
    elif function == test2:
        print("\n Tearing Down test2")
    else:
        print("\n Tearing Down unknown test")

def test1():
    print("\n Executing test1")
    assert True


def test2():
    print("\n Executing test2")
    assert True
