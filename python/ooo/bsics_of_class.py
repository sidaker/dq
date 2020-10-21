import pytest
# https://runestone.academy/runestone/books/published/pythonds/Introduction/ObjectOrientedProgramminginPythonDefiningClasses.html
# ?? Why you create new classes as program?
# create new classes that model data that is needed to solve the problem.
# Whenever we want to implement an abstract data type, we will do so with a new class.
# ?? CASING : Camel case like Fraction , Time , String etc.
# As a minimum implement __str__() and __repr__() methods. why?
# Which methods need self as anargument? which don't?
# If it is a list or any class that holds  elements then also implement __lt__
# and __eq__ methods as a minimum.
# self is a special parameter that will always be used as a reference back to the object itself.

# As of Python 3.5, gcd is in the math module;
def gcdfunc(m, n):
    '''
    Euclid’s Algorithm states that the greatest common divisor of two integers 𝑚 and 𝑛 is 𝑛 if 𝑛 divides 𝑚 evenly.
    However, if 𝑛 does not divide 𝑚 evenly, then the answer is the
    greatest common divisor of 𝑛 and the remainder of 𝑚 divided by 𝑛.
    '''

    while n:
      m, n = n, m%n
    return m


class Fraction:

    # the constructor.
    def __init__(self, top, bottom):
        # self.num in the constructor defines the fraction object to have an
        # internal data object called num as part of its state.
        # it must always be the first formal parameter.
        self.num = top
        self.denom = bottom
        # The values of the two formal parameters top, bottom, are initially assigned to the
        # state, allowing the new fraction object to know its starting value.


    def __str__(self):
    #    # if not implemented: TypeError: __str__ returned non-string (type NoneType)
    #    return "yet to implement"
        '''
        In Python, all classes have a set of standard methods that are provided but may not work properly.
        One of these, __str__, is the method to convert an object into a string.
        The default implementation for this method is to return the instance address string as we have already seen.
        What we need to do is provide a “better” implementation for this method.
        '''
        return str(self.num)+"/"+str(self.denom)


    # def __repr__(self):
    #     pass
    #
    #

    
    def __add__(self, otherfraction):
        '''
        The addition function returns a new Fraction object with the numerator and denominator of the sum
        f1 + f2  f1 is represented by self and f2 by other fraction
        '''
        newnum = self.num*otherfraction.denom + self.denom*otherfraction.num
        newdenom = self.denom * otherfraction.denom
        # print(newnum)
        # print(newdenom)
        # get GCD to reduce fractions for “lowest terms” representation.
        gcd = gcdfunc(newnum, newdenom)
        return Fraction(newnum//gcd,newdenom//gcd)

    def __sub__(self):
        pass


    def __eq__(self, otherfraction):
        '''override __eq__ method. The __eq__ method is another standard method available in any class.
        The __eq__ method compares two objects and returns True if their values are the same, False otherwise.
        '''
        fnum = self.num*otherfraction.denom + self.denom*otherfraction.num
        snum = self.denom * otherfraction.denom

        return fnum == snum


if __name__ == '__main__':
    myfraction = Fraction(3,5)
    print(myfraction)
    f1 = Fraction(1,4)
    f2 = Fraction(1,2)

    f3 = Fraction(1,2)
    f4 = Fraction(2,4)
    print(f1+f2)

    '''
    From command line/Atom if you have not implemented  __repr__(self) and __str__(self)
    (base) hodqadms-MacBook-Pro:ooo sbommireddy$ python bsics_of_class.py
    <__main__.Fraction object at 0x1014a6750>
    The fraction object, myf, does not know how to respond to this request to print.
    The print function requires that the object convert itself into a string so that
    the string can be written to the output. The only choice myf has is to show the
    actual reference that is stored in the variable (the address itself). This is not what we want.
    '''

    assert gcdfunc(2, 4) == 2
    assert gcdfunc(4, 2) == 2
    assert gcdfunc(200, 4) == 4
    assert gcdfunc(2, 3) == 1
    assert gcdfunc(200, 60) == 20
    assert gcdfunc(1, 4) == 1
    print(gcdfunc(6, 8))
    # print(6/2)
    # print(6//2)
    print(f1 == f2)
    print(f3 == f4)
