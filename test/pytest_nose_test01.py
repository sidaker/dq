'''
python -m pytest pytest_nose_test01.py
python -m nose pytest_nose_test01.py
py.test pytest_nose_test01.py
py.test tests
'''
def test_case01():
    assert 'python'.upper() == 'PYTHON'

def test_case02():
    assert 'python'.lower() == 'chikki'
