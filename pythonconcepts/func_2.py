from urllib.request import urlopen
'''
__name__ is a specially named variable allowing us to detect
whether a module is run as a script or imported into another
module.
module code is executed only once on first import.

Access to commandline arguments in python is through
the attribute of the sys module called argv which is a list of strings.
to use it we must import sys module.
'''

def fetch_words():
    # XXX:
    story_words = []

    with urlopen("http://sixty-north.com/c/t.txt") as story:
        for line in story:
            line_words = line.decode('utf-8').split()

            for word in line_words:
                story_words.append(word)


print(__name__)

if(__name__ == '__main__' ):
    fetch_words()
