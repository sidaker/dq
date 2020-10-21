aName='sid'
age=34
# https://runestone.academy/runestone/books/published/pythonds/Introduction/InputandOutput.html

print("Hello","World")
#Hello World
print("Hello","World", sep="***")
#Hello***World
print("Hello","World", end="***")

#Hello World***>>>
#aName = input('Please enter your name: ')

#The % operator is a string operator called the format operator.
#the %s specifies a string, while the %d specifies an integer.
#Other possible type specifications include i, u, f, e, g, c, or %.
print("%s is %d years old." % (aName, age))

itemdict = {"item":"banana","cost":24}
print("The %(item)s costs %(cost)7.1f cents"%itemdict)
