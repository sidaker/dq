
# CASE1 : Filter a list of dictionaries
l = [{'key':10}, {'key':4}, {'key':8}]

def condition(dic):
    ''' Define your own condition here'''
    return dic['key'] > 7

filtered = [d for d in l if condition(d)]

print(filtered)
# [{'key': 10}, {'key': 8}]
