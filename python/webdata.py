#import urllib.request
#response = urllib.request.urlopen('https://www.google.com/')
from urllib import request,error,parse

response = request.urlopen('https://www.google.com/')
print("The output of the URL is:\n\n",response.read())
print("Result Code" + str(response.getcode())) # 200
#data = response.read()
#print(data)
print("*"*50)

# Parsing URL using urlparse()
urlParse = parse.urlparse('https://linuxhint.com/play_sound_python/')
print("\nThe output of URL after parsing:\n", urlParse)

# Joining URL using urlunparse()
urlUnparse = parse.urlunparse(urlParse)
print("\nThe joining output of parsing URL:\n", urlUnparse)

# Parsing URL using urlsplit()
urlSplit = parse.urlsplit('https://linuxhint.com/play_sound_python/')
print("\nThe output of URL after splitting:\n", urlSplit)

# Joining URL using urlunsplit()
urlUnsplit = parse.urlunsplit(urlSplit)
print("\nThe joining output of splitting URL:\n",urlUnsplit)


# Open the URL for reading
urlResponse = request.urlopen('https://linuxhint.com/python_pause_user_input/')
# Reading response header output of the URL
print(urlResponse.info())

# Reading header information separately
print('Response server = ', urlResponse.info()["Server"])
print('Response date is = ', urlResponse.info()["Date"])
print('Response content type is = ', urlResponse.info()["Content-Type"])


# try block to open any URL for reading
try:
   #url = input("Enter any URL address: ")
   url = "https://www.bbc.co.uk/sport/football/543899889"
   response = request.urlopen(url)
   print(response.read())

# Catch the URL error that will generate when opening any URL
except error.URLError as e:
   print("URL Error:",e.reason) # URL Error: Internal Server Error
# Catch the invalid URL error
except ValueError:
  print("Enter a valid URL address")

# Take input any valid URL
#url = input("Enter any URL address: ")
url = "https://www.bbc.co.uk/sport/football/543899889"
# Send request for the URL
request1 = request.Request(url)
print("*"*50)
print(request1)

try:
 # Try to open the URL
 request.urlopen(request1)
 print("URL Exist")
except error.HTTPError as e:
 # Print the error code and error reason
 print("Error code:%d\nError reason:%s" %(e.code,e.reason))

# An HTMLError generates when the given URL address does not exist.
# If the address does not exist, then an URLError exception will be raised and the reason for the error will print. If the value of the URL is in an invalid format, then a ValueError will be raised and the custom error will print.
