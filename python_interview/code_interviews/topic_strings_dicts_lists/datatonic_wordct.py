## https://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
def func(s):
    '''read a string, split '''
    result = {}
    for key in s.split():
        #print(key)
        if(key in result):
            # Exists and add to count.
            result[key] = result.get(key, 0) + 1
            #print(result[key])
        else:
            # new and add to dict
            #print("Key not found", key)
            result[key] = 1

    #print(result)
    return result


if __name__ == '__main__':
    a = "I I want to know how many times each words occurs in a string. I want you to write a python program. how you decide"
    print(func(a))
