'''
This is a Python program that computes word count
    - per line
    - total words in the file
This program needs an understanding of below
    - for loop
    - string split function
    - variables (local and global scope)
    - functions
    - generators
    - Reading a file using with
    - Difference between yield and return
'''

filepath = "/Users/siddharthabommireddy/Desktop/Python/sidgitrepo/dq/pyspark/welcome.txt"

def wordcount(line):
    ct=0
    for word in line.split():
        ct = ct +1
    return ct

def readfile(fullfilepath):
    '''
    Read each line of the file and return it
    to calling function using yield.
    '''
    with open(fullfilepath) as fp:
        for line in fp:
            yield line

def main():
    overall_ct = 0
    for no,line in enumerate(readfile(filepath),1):
        wc = wordcount(line)
        # using format() method
        print('Line {} has a total of "{}!"'.format(no, wc))
        print(line)
        overall_ct = overall_ct + wc
    print('Total number of words {}'.format(overall_ct))

if __name__ == '__main__':
    main()
