def sum(a,b):
  '''
  This is a simple program to explain use of docstring.This function adds two numbers
  '''
  return a+b

def main():
    ''' This is main function'''

    print(sum(22,3))
    print(sum.__doc__)
    #help(sum)

    for i in [1,2,3,4]:
        print(i)

    for c,i in enumerate([1,2,3,4]):
        print('Iteration {0} Value is {1}'.format(c,i))

if __name__ == '__main__':
    main()
