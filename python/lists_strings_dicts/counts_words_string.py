import sys
import operator

# Problem : Get counts of every word in a string.
a = 'one two two three three three four four four four three'
worddict = {}
for i in a.split():
    #print(i)
    if(worddict.get(i, None) in worddict.values()):
        worddict[i] += 1
    else:
        worddict[i] = 1

worddict1 = {}
for i in a.split():
    try:
        worddict1[i] += 1
    except KeyError:
        worddict1[i] = 1
    except:
        print("Unpected error:",sys.exc_info()[0])

# https://docs.python.org/3/tutorial/errors.html

worddict2 = {}
for i in a.split():
    #print(i)
    if(i in worddict2.keys()):
        worddict2[i] += 1
    else:
        worddict2[i] = 1

print(worddict)
print(worddict1)
print(worddict2)

# Problem : Get the key with maximum value.
# Get the word with most/least number of occurences
# flip keys and values in a dictionary
# This can be a problem if there are duplicate values. How do you handle?

#Solution 1:

inverse = [(value, key) for key, value in worddict.items()]
print(inverse)
print(max(inverse))
print(min(inverse))

#Solution 2:
print(max(worddict.items(), key=operator.itemgetter(1))[0])

#Solution 3: Most elegant
print(max(worddict, key=worddict.get))
print(min(worddict, key=worddict.get))
