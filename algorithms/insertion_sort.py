import pytest
# pytest insertion_sort.py -v

def insertionSort(alist):
   for index in range(1,len(alist)):

     #element to be compared
     currentvalue = alist[index]
     position = index # You can manage with just the index variable.

     #comparing the current element with the sorted portion and swapping
     # Move elements of alist[0..index-1], that are
     # greater than currentvalue, to one position ahead
     # of their current position
     while position>0 and alist[position-1]>currentvalue:
         alist[position]=alist[position-1]
         position = position-1

     alist[position]=currentvalue

   return alist


def insertionSort1(alist):

   for i in range(1,len(alist)):

       #element to be compared
       current = alist[i]

       #comparing the current element with the sorted portion and swapping
       while i>0 and alist[i-1]>current:
           alist[i] = alist[i-1]
           i = i-1
       alist[i] = current

       #print(alist)

   return alist

def test_positive():
    assert insertionSort([1,2,3,4]) == [1,2,3,4]
    assert insertionSort([4,3,2,1]) == [1,2,3,4]
    assert insertionSort([1,9,5,4,2]) == [1,2,4,5,9]
    assert insertionSort([54,26,93,17,77,31,44,55,20]) == [17, 20, 26, 31, 44, 54, 55, 77, 93]

    assert insertionSort1([1,2,3,4]) == [1,2,3,4]
    assert insertionSort1([4,3,2,1]) == [1,2,3,4]
    assert insertionSort1([1,9,5,4,2]) == [1,2,4,5,9]
    assert insertionSort1([54,26,93,17,77,31,44,55,20]) == [17, 20, 26, 31, 44, 54, 55, 77, 93]

@pytest.mark.xfail
def test_negative():
    assert insertionSort([4,3,2,1]) == [4,3,2,1] # expected to fail.
    assert insertionSort([1,2,3,4]) == [1,5,3,4] # expected to fail.

    assert insertionSort1([4,3,2,1]) == [4,3,2,1] # expected to fail.
    assert insertionSort1([1,2,3,4]) == [1,5,3,4] # expected to fail.

if __name__ == '__main__':
    list1 = [56,55,45,67,43,33]
    print("Hello")
    print(insertionSort(list1))
    print(insertionSort1(list1))
