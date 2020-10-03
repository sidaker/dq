from html.parser import HTMLParser
from urllib import request,error,parse

metacount = 0

# Create our own HTML Parser based on python's HTMLParser class.
# Overriding the HTMLParser class.

class MyHTMLParser(HTMLParser):
    def handle_comment(self, data):
        print("Encountered  comment:", data)
        pos = self.getpos()
        #print(pos)
        print("\tAt line:", pos[0], "position ", pos[1])

    def handle_starttag(self, tag, attrs):
        if(tag == 'meta'):
            global metacount
            metacount += 1
        print("Encountered  start tag:", tag)
        pos = self.getpos()
        #print(pos)
        print("\tAt line:", pos[0], "position ", pos[1])

        # check for attributes in start tag.
        if(attrs.__len__() > 0):
            print("\t Attributes")
            for a in attrs:
                print("\t", a[0], "=", a[1])

    def handle_endtag(self, tag):
        print("Encountered  end tag:", tag)
        pos = self.getpos()
        #print(pos)
        print("\tAt line:", pos[0], "position ", pos[1])

    def handle_data(self, data):
        print("Encountered  data:", data)
        if(data.isspace()):
            return
        pos = self.getpos()
        print(pos)
        print("\tAt line:", pos[0], "position ", pos[1])



def main():
    parser = MyHTMLParser()
    #response = request.urlopen('https://www.google.com/')
    fullpath = '/Users/sbommireddy/Documents/python/assignments/dq/python/test.html'
    f = open(fullpath)
    if f.mode == 'r':
        contents =  f.read()
        parser.feed(contents)

    print("Meta tags:", str(metacount))


if __name__ == '__main__':
    main()
