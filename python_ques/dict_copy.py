# dictionary keys must be immutable
# str, int etc are acceptable but not lists.
# shallow copy (default) of dictionaries.

a = {1:'sid', 2:'Advik', 3:'Lik'}
newdict = dict(a)
newdict1 = a.copy()

print(a is newdict)
print(a is newdict1)
print(a[1] is newdict[1]) # Each key of both dictionaries refer to same object.
print(a[1] is newdict1[1]) # Each key of both dictionaries refer to same object.
