def filterFunc(x):
    if x % 2 == 0:
        return False
    return True

def filterFunc2(x):
    if x.islower():
        return True
    return False

def squareFunc(x):
    return x**2

def toGrade():
    pass



def main():
    nums = (1,8,4,5,6,88,65,44,5,381,480)
    chars = "abcDeFGHiJklmnopQRSt"
    grades = (81,89,94,78,61,66,99,75)

    #map
    sq2 = list(map(squareFunc,nums))
    print(sq2)

    #filter
    odds = list(filter(filterFunc,nums))
    print(odds)

    lowers = list(filter(filterFunc2,chars))
    print(lowers)
    #sorted.
    grades  = sorted(grades)
    print(grades)

if __name__ == '__main__':
    main()
