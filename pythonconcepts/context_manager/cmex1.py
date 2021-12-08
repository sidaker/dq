'''
with expression as x:
    body

the value of expression.__enter__() is bount to x.
not the value of expression.

the expression must evaluate to a context manager, that is the expression must
produce an object which supports both the _ _enter_ _ and _ _exit_ _ methods.
Once the expression is evaluated and we have a context manager object, the with statement
then calls _ _enter_ _ on the context manager with no arguments.
If _ _enter_ _ throws an exception, execution never enters the with block and the
with statement is done.
Assuming that _ _enter_ _ executes successfully, it can return a value.
If the with statement includes an as clause, this return value is bound to the name
in the as clause; otherwise, this return value is discarded.

it's actually the return value of the context manager's _ _enter_ _ that is bound to the as variable.
'''

'''
In many cases, in fact, _ _enter_ _ simply returns the context manager itself. But this is not always the case, so it's important to keep in mind what's really happening. Once _ _enter_ _ has been executed and its return value potentially bound to a name, the with block itself is executed. The with block can terminate in one of two fundamental ways, with an exception or by running off the end of the block, which we call normal termination. In both cases, the context manager's _ _exit_ _ method is called after the block. If the block exits normally, _ _exit_ _ is called with no extra information. If, on the other hand, the block exits exceptionally, then the exception information is passed to _ _exit_ _.

Context managers are objects that have both _ _enter_ _ and _ _exit_ _ methods The main use of context managers is for properly managing resources. The expression in a with‑statement must evaluate to a context manager object. The with‑statement calls its context managers _ _enter_ _ method before entering the with‑block. The return value of _ _enter_ _ is bound to the as‑variable of the with‑statement if it's defined. _ _exit_ _ is called after the with‑block is complete. If the with‑block exits with an exception, the exception information is passed to _ _exit_ _. _ _exit_ _ can control the propagation of an exception by returning false to propagate it, or true to swallow it. The with‑statement is syntactic sugar for much larger and more complicated body of code. 
'''
