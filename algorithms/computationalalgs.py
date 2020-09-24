'''
Find if a number is prime or not.
Find if a given word is a palindrome
Progression Algorithms -> Arithmentic, Geometric and Fibinocci
Euclid's GCD of two integers
power with recursion
factoria with recursion
'''
import pytest

def gcd(a,b):
    while(b !=0):
        t = a
        a = b
        b = t%b # As long
    return a

def fibi():
    pass

def isprime():
    pass

def ispal():
    pass

def factorial(n):

    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def power(num,pwr):

    if pwr == 0:
        return 1
    else:
        return num * power(num,pwr-1)

if __name__ == '__main__':
    assert gcd(60,96) == 12
    assert gcd(20,8) == 4
    assert gcd(20,1) == 1
    assert gcd(120,240) == 120
    assert factorial(5) == 120
    assert factorial(3) == 6
    assert factorial(0) == 1
    assert power(2,4) ==  16
    print(60%96)
    print(factorial(5))
    print(power(2,3))
