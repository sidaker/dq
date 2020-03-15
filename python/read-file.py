import sys
import os

def main():
   #filepath = sys.argv[1]
   filepath = "parse-xml-csv.py"
   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()


   with open(filepath) as fp:
       for line in fp:
           print("contents {}".format(line))

if __name__ == '__main__':
   main()
