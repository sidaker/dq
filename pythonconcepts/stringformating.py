from string import Template


a = ' world!'
print(f'hello {a}')
print('hello {}{}'.format(a, " By Advik"))

# Template Strings. Use it for straight forward variable substitution.
templ = Template('Let us C by ${author} forward by ${foreword}')
str2 = templ.substitute(author="Sid B",foreword="Yesh K")
print(str2)

data = {
    "author" : 'Sid',
    "foreword" : 'Advanced Python'
}

str3 = templ.substitute(data)
print(str3)

print(range(0))
