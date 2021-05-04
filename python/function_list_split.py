def unmerge(*args):
    # using *arg passing args to a function will make python unpack the values in arg and pass it to the function.
    left = []
    right = []
    print(args)
    print(len(args))
    print(len([12,34,56,78,89]))
    for i in range(0,len(args),2):
        print(i)
        left.append(args[i])
        if(i+1<len(args)):
            right.append(args[i+1])

    return (left,right)



if __name__ == '__main__':
    print(unmerge([12,34,56,78,89]))

    targs = [3, 6]
    print(list(range(*targs)) )           # call with arguments unpacked from a list
    #[3, 4, 5]
