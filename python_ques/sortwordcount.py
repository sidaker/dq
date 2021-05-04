from operator import itemgetter

str='''hello let us count words abs and
word from and let us do it and do it again. god love you.
finally we did it. thank god god is great. god is every where
'''
dict={}
for line in str.split("\n"):
    print(line)
    for word in line.split():
        try:
            dict[word] += 1
        except KeyError:
            dict[word] = 1

print(dict)

sortedWords = sorted(dict.items(), key=itemgetter(1), reverse = True)
print(sortedWords)
