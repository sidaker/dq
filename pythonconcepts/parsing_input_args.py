import sys
from urllib.request import urlopen


'''
Access to commandline arguments in python is through
the attribute of the sys module called argv which is a list of strings.
to use it we must import sys module.

python parsing_input_args.py "http://sixty-north.com/c/t.txt"

Refer doc opt and argparse modules for sophisticated
argument processing.

'''

def fetch_words(url):
    '''
    Help about this function
    '''
    story_words = []

    with urlopen(url) as story:
        for line in story:
            line_words = line.decode('utf-8').split()

            for word in line_words:
                story_words.append(word)

    return story_words


def print_items(items):
    for item in items:
        print(item)


def main():
    url =  sys.argv[1]
    words =  fetch_words(url)
    print_items(words)

if(__name__ == '__main__' ):
    main()
