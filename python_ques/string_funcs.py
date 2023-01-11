import re

# Handling multiple delimiters for split
line = 'asdf fjdk; afed, fjek,asdf, foo'
li = re.split(f'[;,\s]\s*', line)
print(li)
li1 = re.split(r'(?:,|;|\s)\s*', line)
print(li1)

filenames=[ 'Makefile', 'foo.c', 'bar.py', 'spam.c', 'spam.h' ]
progfiles = [f for f in filenames if f.endswith(('.c','.py')) ]
print(progfiles)

from fnmatch import fnmatch, fnmatchcase
print(fnmatch('foo.txt', '*.txt'))

names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']
print([name for name in names if fnmatch(name, 'Dat*.csv')])

text = 'yeah, but no, but yeah, but no, but yeah'
print(text.find('no'))

text1 = '11/27/2012'
text2 = 'Nov 27, 2012'

# Simple matching: \d+ means match one or more digits >>>
if re.match(r'\d+/\d+/\d+', text1):
    print('yes')
else:
    print('nooo')

datepat = re.compile(f'\d+/\d+/\d+')
if datepat.match(text1):
    print('yesss pre compiled regex')
else:
    print('nooo')

text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
print(datepat.findall(text))

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
m = datepat.match('11/27/2012')
print(m.group(0))
print(m.group(1))


text = 'yeah, but no, but yeah, but no, but yeah'
text.replace('yeah', 'yep')

text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
print(re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text))
## Backslashed digits such as \3 refer to capture group numbers in the pattern.
