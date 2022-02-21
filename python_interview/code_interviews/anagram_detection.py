'''
One string is an anagram of another if the second is simply a rearrangement of the first.
Anagram examples:
'heart' and 'earth' are anagrams
Same number of elements
Same count of individual elements
e.g. length of 5 and one occurence of e,a,r,t,h
'''

def letter_counter(word):
    #
    letterdict = {}
    # iteration of dict is O(n)
    for i in word:
        #print(i)
        # in is O(1)
        # contains operator for lists is 𝑂(𝑛) and the contains operator for dictionaries is 𝑂(1).
        if(letterdict.get(i, None) in letterdict.values()):
            letterdict[i] += 1
        else:
            letterdict[i] = 1
    return letterdict

def anag_check1(w1, w2):
    # check for no of occurences of each element
    # Count and Compare
    if(len(w1) != len(w2)):
        print(f"Unequal lengths: word {w1} and word {w2}")
        return False


    # call a function that takes a word a returns a dictionary
    # of no of occurences of each element
    dict1 = letter_counter(w1)
    dict2 = letter_counter(w2)

    # Compare two dicts and even if one of the keys have a different values it is not an anagram.
    # Both dictionaries should have same keys
    for key in dict1.keys():
        if key not in dict2:
            print(f"{key} from word {w1} not found in word {w2}")
            return False
    return True



def anagram_check_ct_cmp_withoutdict(s1,s2):
    # Big(O) n
    c1 = [0]*26
    c2 = [0]*26

    for i in range(len(s1)):
        # ord('a') 97
        # ord('b') - ord('a') 1
        pos = ord(s1[i])-ord('a')
        c1[pos] = c1[pos] + 1

    for i in range(len(s2)):
        pos = ord(s2[i])-ord('a')
        c2[pos] = c2[pos] + 1

    j = 0
    stillOK = True
    while j<26 and stillOK:
        if c1[j]==c2[j]:
            j = j + 1
        else:
            stillOK = False

    return stillOK


def anag_check1_sort_compare(s1,s2):
    '''
    At first glance you may be tempted to think that this algorithm is 𝑂(𝑛), since there is one simple iteration to compare the n characters after the sorting process. However, the two calls to the Python sort method are not without their own cost. As we will see in a later chapter, sorting is typically either 𝑂(𝑛2) or 𝑂(𝑛log𝑛), so the sorting operations dominate the iteration. In the end, this algorithm will have the same order of magnitude as that of the sorting process.
    '''
    alist1 = list(s1)
    alist2 = list(s2)

    alist1.sort()
    alist2.sort()

    pos = 0
    matches = True

    while pos < len(s1) and matches:
        if alist1[pos]==alist2[pos]:
            pos = pos + 1
        else:
            matches = False

    return matches

if __name__ == '__main__':
    print(anag_check1('hello','bolo'))
    print(anag_check1('hell','bolo'))
    print(anag_check1('heart','earth'))

    print("*"*50)

    print(anagram_check_ct_cmp_withoutdict('hello','bolo'))
    print(anagram_check_ct_cmp_withoutdict('hell','bolo'))
    print(anagram_check_ct_cmp_withoutdict('heart','earth'))

    print("*"*50)
    print(anag_check1_sort_compare('hello','bolo'))
    print(anag_check1_sort_compare('hell','bolo'))
    print(anag_check1_sort_compare('heart','earth'))
