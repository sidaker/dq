def bubbsort(lista):

    for elem in range(len(lista)-1,0,-1):
        #make n-1 passes worst case.
        exchFlag = True
        for i in range(0,elem):
            if lista[i] > lista[i+1]:
                lista[i] , lista[i+1] = lista[i+1] , lista[i]
                exchFlag = False

        if exchFlag:
            #print("No Exchnage took place")
            break
    return lista

def mergsort(listb):
    '''Uses recursion and Divide and Conquer'''
    print("Splitting ",listb)
    ### You need to stop recusrion at some point and need to have a condition.
    ### You stop when the list has 1 element. Divide till you get 1 element.
    ###  If the length of the list is less than or equal to one, then we already have a sorted list and no more processing is necessary.
    if len(listb)>1:
        # Let us split into 2 lists using list slicing

        middle_index = len(listb)//2
        leftlist = listb[:middle_index]
        rightlist = listb[middle_index:]
        mergsort(leftlist)
        mergsort(rightlist)

        # Now sort and merge.
        i = 0
        j = 0
        k = 0

        ####
        ## Notice that the merge operation places the items back into the original list
        ## (listb) one at a time by repeatedly taking the smallest item from the sorted lists.
        while i < len(leftlist) and j < len(rightlist):
            if(leftlist[i] <= rightlist[j] ) :
                listb[k] = leftlist[i]
                i = i +1
                k = k + 1
            else:
                listb[k] = rightlist[j]
                j = j +1
                k = k + 1

        # add remain elements of left list
        while i<len(leftlist):
            listb[k] = leftlist[i]
            i = i +1
            k = k + 1

        # add remain elements of right list
        # add remain elements of left list
        while j<len(rightlist):
            listb[k] = rightlist[j]
            j = j +1
            k = k + 1
    print("Merging ",listb)
    return listb




if __name__ == '__main__':
    list1 = [2,5,3,7,1]
    list2 = [1,2,3]
    list3 = [12,5,3,7,14,13,33,45,3,32,30]
    print(bubbsort(list1))
    print(mergsort(list1))
    print(bubbsort(list2))
    print(mergsort(list2))
    print(bubbsort(list3))
    print(mergsort(list3))
