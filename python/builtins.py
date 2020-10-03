
def usebuiltins():
    if any([1,2,3,4,5,0]):
        print("Atleast one element is True")

    if all([1,2,3,4,5,6]):
        print("All elements are True")

    if any([0,0]):
        print("No element is True.Will never be printed")

    if all([1,3,4,5,0]):
        print("atleast one element is False.Will never be printed")

    if [0,0]:
        print("List is not empty.")

    print(sum([1,2,3,4,5,6]))
    print(max([1,2,3,4,5,6]))
    print(min([1,2,3,4,5,6]))
    print(abs(0.2))
    print(abs(-22))
    print(hash("hello"))
    print(pow(2,3))
    print(set(2,3))

if __name__ == '__main__':
    usebuiltins()
