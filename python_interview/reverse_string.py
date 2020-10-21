'''Write a function revstring(mystr) that uses a stack to reverse the characters
in a string.
'''

def strrev1(s1):
    s2 = ''
    for i in s1:
        s2 = i + s2
    return s2

def reverse_join_reversed_iter(s):
    s1 = ''.join(reversed(s))
    return s1

def use_list_rev(s):
    temp_list = list(s)
    temp_list.reverse()
    return ''.join(temp_list)  

if __name__ == '__main__':

    s1 = "abcde"
    # reverse method 1
    # Create a slice that starts at the end of the string, and moves backwards.
    # In this particular example, the slice statement [::-1] means start at the
    # end of the string and end at position 0, move with the step -1, negative one, which means one step backwards.
    print(s1[::-1])
    # print(s1[1:4:2]) # starts at index 1 and ends before index 4 with a step of 2

    # reverse method 2
    print(strrev1(s1))

    # reverse method 3
    print(reverse_join_reversed_iter(s1))

    # using list reverse
    print(use_list_rev(s1))
