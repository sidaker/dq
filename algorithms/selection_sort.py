import pytest
# pytest selection_sort.py -v

'''
Pass        Comparisons
1           n-1
2           n-2
..          ...
n-2         2
n-1         1

The selection sort improves on the bubble sort by making only one exchange
for every pass through the list.

In order to do this, a selection sort looks for the largest value as it
makes a pass and, after completing the pass, places it in the proper
location. As with a bubble sort, after the first pass, the largest item is in
the correct place. After the second pass, the next largest is in place.
This process continues and requires 𝑛−1 passes to sort n items,
since the final item must be in place after the (𝑛−1) st pass.

'''


def selectsort(dataset):

    for i in range(len(dataset)-1,0,-1):
        positionOfMax=0
        for location in range(1,i+1):
            if(dataset[location]>dataset[positionOfMax]):
                positionOfMax = location

        print(f'Pass No {i}: Exchanging {location}  and {positionOfMax} ')
        dataset[location], dataset[positionOfMax] = dataset[positionOfMax],dataset[location]

    return dataset

def test_positive():
    assert selectsort([1,2,3,4]) == [1,2,3,4]
    assert selectsort([4,3,2,1]) == [1,2,3,4]
    assert selectsort([1,9,5,4,2]) == [1,2,4,5,9]

@pytest.mark.xfail
def test_negative():
    assert selectsort([4,3,2,1]) == [4,3,2,1] # expected to fail.
    assert selectsort([1,2,3,4]) == [1,5,3,4] # expected to fail.

if __name__ == '__main__':
    list1 = [56,55,45,67,43,33]
    print("Hello")
    print(selectsort(list1))
