import pytest

pytest test_quicksort.py -v
'''
There are many different versions of quickSort that pick pivot
in different ways.

    - Always pick first element as pivot.
    - Always pick last element as pivot (implemented below)
    - Pick a random element as pivot.
    - Pick median as pivot.

The key process in quickSort is partition().
Target of partitions is, given an array and an element x of array as pivot,
put x at its correct position in sorted array and
put all smaller elements (smaller than x) before x, and
put all greater elements (greater than x) after x.
All this should be done in linear time.
'''

'''
    # Sort happens in place
    # Identify pivot
    # Divide and Conquer and uses recursion
    # Performs better than merge sort.
    # All the work gets done in the partition step.
'''

def quick_sort_ltelem_pivot(dataset):
    pass

def quick_sort_randelem_pivot(dataset):
    pass

def test_positive_lt():
    assert quick_sort_ltelem_pivot([1,2,3,4]) == [1,2,3,4]
    assert quick_sort_ltelem_pivot([4,3,2,1]) == [1,2,3,4]
    assert quick_sort_ltelem_pivot([1,9,5,4,2]) == [1,2,4,5,9]

@pytest.mark.xfail
def test_negative_lt():
    assert quick_sort_ltelem_pivot([4,3,2,1]) == [4,3,2,1] # expected to fail.
    assert quick_sort_ltelem_pivot([1,2,3,4]) == [1,5,3,4] # expected to fail.


def test_positive_rande():
    assert quick_sort_randelem_pivot([1,2,3,4]) == [1,2,3,4]
    assert quick_sort_randelem_pivot([4,3,2,1]) == [1,2,3,4]
    assert quick_sort_randelem_pivot([1,9,5,4,2]) == [1,2,4,5,9]

@pytest.mark.xfail
def test_negative_rande():
    assert quick_sort_randelem_pivot([4,3,2,1]) == [4,3,2,1] # expected to fail.
    assert quick_sort_randelem_pivot([1,2,3,4]) == [1,5,3,4] # expected to fail.
