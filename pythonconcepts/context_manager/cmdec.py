'''
While it's sometimes necessary to implement context managers as classes implementing
the protocol, that can be unwieldy for many simple context managers.
Fortunately, the standard library provides a simpler mechanism that you can use in many situations.
we look at the contextmanager decorator from the standard library contextlib module.

The idea behind context manager is simple. You define a generator that is a
function, which uses yield instead of return, and decorate it with the contextmanager
decorator to create a context manager factory.
This factory is nothing more than a callable object, which returns context managers,
making it suitable for use in a with statement.
'''
import contextlib
import sys

@contextlib.contextmanager
def mycxm():
    try:
        '''
        the contextmanager decorator allows you to define context managers using normal flow control by the yield statement rather than breaking it up across two methods.
        Furthermore, since generators remember their state between calls to yield, you don't need to define a new class just to create a stateful context manager.
         Unlike standard context managers, those created with the contextmanager decorator must use normal exception handling to determine if exceptions are propagated from the with statement. If the context manager function propagates the exception either via reraising it or by simply not catching it at all, then the exception will propagate out of the statement. If the context manager catches and doesn't reraise the exception from the with block, then the exception won't be propagated out of the with statement
        '''
        yield "you're in with block"
        ## FROM HERE NORMAL EXIT
        print("LoggingContextManager.__exit__: normal exit")
    except:
        ## Exceptional EXIT
        print('Exception detected by LoggingContextManager.__exit__',
               sys.exc_info())
        raise

with mycxm() as x:
    raise ValueError()
