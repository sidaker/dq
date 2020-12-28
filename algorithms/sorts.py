'''
Bubble Sort -> Basic. Don't use it at all. O n2 O n square.
Quick Sort ->  Uses recursion. Better than Merge Sort.
Merge Sort ->  Uses recursion. Divide and Conquer. n log n.

'''

def bubblesort(dataset):
    '''
    Pass        Comparisons
    1           n-1
    2           n-2
    ..          ...
    n-2         2
    n-1         1
    '''
    for i in range(len(dataset)-1,0,-1):
        for j in range(i):
            if(dataset[j] > dataset[j+1]):
                #swap
                dataset[j+1], dataset[j] = dataset[j],dataset[j+1]
        print("current state: ", dataset)


def mergesort(dataset):
    if(len(dataset)>1):
        mid = len(dataset) // 2
        leftarr = dataset[:mid]
        rightarr = dataset[mid:]

        # Recursively breakdown arrays
        mergesort(leftarr)
        mergesort(rightarr)

        # Perform Merging
        i=0 # index into l array
        j=0 # index into r array
        k=0 # index into merged array

        # While both arrays have content
        while(i< len(leftarr) and j< len(rightarr)):
            if(leftarr[i] < rightarr[j]):
                dataset[k] = leftarr[i]
                i += 1
            else:
                dataset[k] = rightarr[j]
                j += 1
            k += 1


        # If the left array still has values add them.
        while(i< len(leftarr)):
            dataset[k] = leftarr[i]
            i += 1
            k += 1

        # If the right array still has values add them.
        while(j< len(rightarr)):
            dataset[k] = rightarr[j]
            j += 1
            k += 1

def quicksort(dataset):

    # Sort happens in place
    # Identify pivot
    # Divide and Conquer and uses recursion
    # Performs better than merge sort.
    # All the work gets done in the partition step.



if __name__ == '__main__':
    list1 = [56,55,45,67,43,33]
    bubblesort(list1)
    print("*"*50)
    print(list1)

    list2 = [56,55,45,67,43,33]
    mergesort(list2)
    print("*"*50)
    print(list2)
