'''
get() method returns a default value if the key is missing.

However, if the key is not found when you use dict[key],
KeyError exception is raised.

'''
# in is the intended way to test for the existence of a key in a dict.

d = {"key1": 10, "key2": 23}

if "key1" in d:
    print("this will execute")

if "nonexistent key" in d:
    print("this will not")

# If you wanted a default, you can always use dict.get():
d = dict()
for i in range(100):
    key = i % 10
    d[key] = d.get(key, 0) + 1
print(d)

person = {'name': 'Phill', 'age': 22}

print('Name: ', person.get('name'))
print('Age: ', person.get('age'))

# value is not provided
print('Salary: ', person.get('salary'))
