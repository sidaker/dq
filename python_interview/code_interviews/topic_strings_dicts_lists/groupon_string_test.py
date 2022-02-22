test_list = ["1234567890", 1234, "ss@test.com", "ss@test", "Hello", 1234567890]
output_list = ['Phone Number', 'Invalid', 'Email', 'Invalid', 'Invalid', 'Phone Number']
domains = (".org", ".com", ".co.uk",".co.ie")
import collections

print(type(domains)) ## tuple
## https://www.askpython.com/python/string/python-string-contains
# https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method

def func1(list1):
    for i,j in enumerate(list1):
        #print(i,j)
        if(isinstance(j, str) and j.isdigit() and len(j)==10):
            list1[i] = "Phone Number"
        elif(isinstance(j, int) and len(str(j))==10):
            list1[i] = "Phone Number"
        #elif(isinstance(j, str) and j.__contains__("@")):
        elif(isinstance(j, str) and '@' in j and j.endswith(domains)):
            list1[i] = "Email"
        else:
            list1[i] = "Invalid"

    return list1


final_list = func1(test_list)
print(final_list)
print(output_list)
if(final_list == output_list):
    print("Lists are identical")

print(collections.Counter(final_list) == collections.Counter(output_list))
