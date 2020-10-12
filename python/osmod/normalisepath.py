from os import path
import pathlib
# https://realpython.com/python-pathlib/
# normalise a path – to remove redundant path entries and collapse parent directories. For example, in Python, we can use Path.resolve:

def is_normalised(path):
    return path == normalise(path)


def normalise(p):
    # return
    return str(pathlib.PosixPath(p).resolve(strict=False)).encode().decode()

if __name__ == '__main__' :
    # call
    normalise('pictures/cat.jpg')
    #'pictures/cat.jpg'
    normalise('pictures//cat.jpg')
    #'pictures/cat.jpg'
    normalise('pictures/./cat.jpg')
    #'pictures/cat.jpg'
    normalise('pictures/pets/../cat.jpg')
    #'pictures/cat.jpg'

    print(is_normalised('pictures//cat.jpg'))
    print(is_normalised('pictures/cat.jpg'))
    print(is_normalised('/Users/sbommireddy/Documents/python/assignments/dq'))
    #normalised paths are distinct and unambigous
    '''
     if you only ever use normalised paths for S3 keys, you can treat S3 keys
     and file paths as interchangeable.

     Introduced a rule that blocks creating S3 objects whose keys aren’t normalised
     paths.
     https://alexwlchan.net/2020/08/s3-keys-are-not-file-paths/
     https://docs.python.org/3/library/pathlib.html
    '''
