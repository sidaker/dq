'''
Sample doctest test module
test_module02
'''

def mul(a, b):
        """
            >>> mul(2, 3)
            6
            >>> mul('a', 2)
            'aa'
        """
        return a * b
def add(a, b):
        """
        >>> add(2, 3)
        5
        >>> add('a', 'b')
        'ab'
        """
        return a + b

# The code below is a simple example of a test module with two functions and two tests for each function.
# python3 -m doctest -v test_module02.py
# Please note indentation is very important
