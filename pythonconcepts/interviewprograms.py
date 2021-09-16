def binarySearch(alist, item):
    found = False
    first = 0
    last = len(alist)-1
    while first<=last and not found:
        # recalculate midpoint every iteration.
        midpoint = (first + last)//2
        if alist[midpoint] == item:
            found = True
        else:
            # recalculate first or last based
            if item < alist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1
    return found


def mergsort(lista):

    if(len(lista)>1):
    # find mid point and split into two list.
        midp = len(lista) // 2
        leftlist = lista[:midp]
        rightlist = lista[midp:]

        mergsort(leftlist)
        mergsort(rightlist)

        i =0
        j =0
        k =0

        while (i < len(leftlist) and j < len(rightlist)):
            if (leftlist[i] <= rightlist[j]):
                lista[k] = leftlist[i]
                i = i + 1
                k = k + 1
            else:
                lista[k] = rightlist[j]
                j = j + 1
                k = k + 1

        # add remaing element from leftlist
        while(i <  len(leftlist)):
            #add
            lista[k] = leftlist[i]
            i = i + 1
            k = k + 1

        # add remaing element from leftlist
        while(j <  len(rightlist)):
            #add
            lista[k] = rightlist[j]
            j = j + 1
            k = k + 1

    #print(lista)
    return lista

if __name__ == '__main__':
    lis1 = [1,5,4,3,6,8,2]
    lis2 = [9,6,8,2]
    lis3 = [4,5,7]
    print(mergsort(lis1))
    print(mergsort(lis2))
    print(mergsort(lis3))

    print(binarySearch(lis1, 3)) # dont use on unsorted lists
    print(binarySearch(lis1, 44)) # dont use on unsorted lists
    print(binarySearch([], 44))
