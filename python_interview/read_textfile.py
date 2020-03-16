import sys
import os

def likhireadfile(filepath):
   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

   with open(filepath) as fp:
       for line in fp:
           print("contents {}".format(line))

if __name__ == '__main__':
   filepath = "/tmp/file.txt"
   likhireadfile(filepath)
