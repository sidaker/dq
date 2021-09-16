import re
a='Beautiful, is; better*than\nugly'
print(re.split('; |, |\*|\n',a))
