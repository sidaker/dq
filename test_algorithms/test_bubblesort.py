
def bubblesort(dataset):
    '''
    Can be improved.Sort till no swaps
    '''
    for i in range(len(dataset)-1,0,-1):
        for j in range(i):
            if(dataset[j] > dataset[j+1]):
                #swap
                dataset[j+1], dataset[j] = dataset[j],dataset[j+1]
        print("current state: ", dataset)
    return dataset

def bubblesort_imp(dataset):
    '''
    Sort till no swaps.
    '''
    for i in range(len(dataset)-1,0,-1):
        swapc = 0
        for j in range(i):
            if(dataset[j] > dataset[j+1]):
                #swap
                swapc += 1
                dataset[j+1], dataset[j] = dataset[j],dataset[j+1]
        print("No of Swaps: ", str(swapc))
        print("current state: ", dataset)
        if(swapc == 0):
            break

    return dataset

def myownbubbsort(listi):
    '''
    Big(O) - Worst case  Complexity - O(n**n)
    Best Case Complexity -
    Average Case Complexity-
    '''
    # Outer for loop.
    # 
    for i in range(len(listi)-1,0,-1):

        swapc = 0
        print(f'PassNo {i}')
        # Inner loop.
        for j in range(len(listi)-1):
            if(listi[j]>listi[j+1]):
                #swap
                 swapc += 1
                 listi[i],listi[j] = listi[j],listi[i]

        if swapc == 0:
            print(f'Total Number of passes {i+1}')
            #return listi # break from outerloop
            break
    print(listi)



if __name__ == '__main__':
    list1 = [1,5,6,3,4,9]
    list2 = [23,5,66,21,44,1]
    list3 = [22,10,1,9,5]
    alreadysorted = [1,2,3,6,9]


    list4 = [1,2,3,4,5]
    list5 = [11,12,31,34,35]

    #print(myownbubbsort(list1))
    #print(myownbubbsort(list2))
    #myownbubbsort(list1)
    #print('*'*50)
    #myownbubbsort(list2)
    #print('*'*50)
    #myownbubbsort(alreadysorted)
    #slist1 = bubblesort(list1)
    #print("Final state: ", slist1)

    # print('*'*50)
    # slist2 = bubblesort(list2)
    # print("Final state: ", slist2)
    # print('*'*50)
    #
    # slist3 = bubblesort(alreadysorted)
    # print("Final state: ", slist3)
    #
    # print('---'*50)
    # print("Initial state: ", list3)
    # implist1 = bubblesort_imp(list3)
    # print("Final state: ", implist1)

    print('---'*50)
    print("Initial state: ", list4)
    implist4 = bubblesort_imp(list4)
    print("Final state: ", implist4)


    print('---'*50)
    print("Initial state: ", list5)
    implist5 = bubblesort(list5)
    print("Final state: ", implist5)

    print('---'*50)
    print("Initial state: ", list2)
    implist2 = bubblesort_imp(list2)
    print("Final state: ", implist2)


    print('---'*50)
    print("Initial state: ", list3)
    implist3 = bubblesort(list3)
    print("Final state: ", implist3)
