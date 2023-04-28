import json
schema1 = json.load(open('api.avsc'))
schema2 = json.load(open('apiv2.avsc'))
def print_cross(s1set, s2set, message):
    for s in s1set:
        if not s in s2set:
            print(message % s)
s1names = set( [ field['name'] for field in schema1['fields'] ] )
s2names = set( [ field['name'] for field in schema2['fields'] ] )
print_cross(s1names, s2names, 'Field "%s" exists in schema1 and does not exist in schema2')
print_cross(s2names, s1names, 'Field "%s" exists in schema2 and does not exist in schema1')
def print_cross2(s1dict, s2dict, message):
    for s in s1dict:
        if s in s2dict:
            if s1dict[s] != s2dict[s]:
                print(message % (s, s1dict[s], s2dict[s]))
s1types = dict( zip( [ field['name'] for field in schema1['fields'] ],  [ str(field['type']) for field in schema1['fields'] ] ) )
s2types = dict( zip( [ field['name'] for field in schema2['fields'] ],  [ str(field['type']) for field in schema2['fields'] ] ) )
print_cross2(s1types, s2types, 'Field "%s" has type "%s" in schema1 and type "%s" in schema2')

'''
for k,v in s1types.items():
    print(k,v)


for k,v in s2types.items():
    print(k,v)
'''

    
