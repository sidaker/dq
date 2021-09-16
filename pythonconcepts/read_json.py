import json

# Opening JSON file
f = open('/Users/sbommireddy/Documents/python/assignments/dq/python/sample.json',)

# returns JSON object as a dictionary

data = json.load(f)
'''
{"true": true}
'''

# Iterating through the json
# list
for i,k in data.items():
    print(i)
    print(type(i))
    print(k)
    print(type(k))

# Closing file
f.close()
