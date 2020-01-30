
# read file.
filename='/Users/sbommireddy/Documents/python/assignments/dq/test/samplefile.txt'

print("*"*50)

with open(filename,'r') as file:
    wordcount={}
    for word in file.read().split():
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
    print (wordcount)
