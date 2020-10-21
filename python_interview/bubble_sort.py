import pytest
# pytest bubble_sort.py -v

'''
Pass        Comparisons
1           n-1
2           n-2
..          ...
n-2         2
n-1         1
'''


def bubblesort(dataset):

    for i in range(len(dataset)-1,0,-1):
        swapc = 0
        for j in range(i):
            if(dataset[j]>dataset[j+1]):
                dataset[j], dataset[j+1] = dataset[j+1] , dataset[j]
                swapc += 1

        if(swapc == 0) :
            # No Swap. List is sorted by now.
            break

    return dataset

def test_positive():
    assert bubblesort([1,2,3,4]) == [1,2,3,4]
    assert bubblesort([4,3,2,1]) == [1,2,3,4]
    assert bubblesort([1,9,5,4,2]) == [1,2,4,5,9]

@pytest.mark.xfail
def test_negative():
    assert bubblesort([4,3,2,1]) == [4,3,2,1] # expected to fail.
    assert bubblesort([1,2,3,4]) == [1,5,3,4] # expected to fail.

if __name__ == '__main__':
    print("Test")
    #test_positive()
    #test_negative()
