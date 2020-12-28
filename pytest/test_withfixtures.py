import pytest

# pytest -v -s test_withfixtures.py
# @pytest.fixture(autouse=True)

@pytest.fixture(scope="session", autouse=True)
def setupDBSession():
    print("\nSetup a Database session. ")

# other scopes include module, function , class

@pytest.fixture()
def setup():
    print("\nSetup")
    yield # code after yield executes fater fixture goes out of scope
    print("\nTeardown")


@pytest.fixture(params=[1,2,3,4])
# params array argument can be used to specify the data returned to the test.
# Test fixtures can thus optionally return data which can be used in the test.
def setup6(request):
    print("\n Setup6")
    retval = request.param
    return retval


@pytest.fixture()
def setup5(request):
    print("\n Setup5")

    def teardown_b():
        print("\n Tear down B")

    def teardown_a():
        print("\n Tear down A")

    request.addfinalizer(teardown_a)
    request.addfinalizer(teardown_b)


def test1(setup5):
    print("Executing test1. Fixture gets executed before this.")
    assert True


def test2():
    print("\nExecuting test2 only")
    assert True

@pytest.mark.usefixtures("setup")
def test3():
    print("Executing test3 and fixture")
    assert True


def test4():
    print("Executing test4 only")
    assert True


def test6(setup6):
    print("Executing test6 with setup retval {}".format(setup6))
    assert True
