from pytest import raises
# pytest -v -s test_asserts.py

def raisesValueException():
    raise ValueError

def test_exception():
    with raises(ValueError):
        raisesValueException()


def test_IntAssert():
    assert 1 == 1


def test_StrAssert():
    assert "str" == "str"


def test_floatAssert():
    assert 0.1 + 0.3 == 0.4

def test_arrAssert():
    assert [1,2,3] == [1,2,3]

def test_listAssert():
    assert [1,2,3,4] == [1,2,3,4]

def test_IntAssert():
    assert {"1" : 1} == {"1" : 1}
