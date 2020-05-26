from urllib.request import urlopen


story_words = []

with urlopen("http://sixty-north.com/c/t.txt") as story:
    for line in story:
        line_words = line.decode('utf-8').split()

        for word in line_words:
            story_words.append(word)


print(story_words)

'''
if you dont put the code in a function.
then the code gets executed when imported
'''
