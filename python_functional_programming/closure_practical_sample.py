import logging
logging.basicConfig(filename='logex.log',level=logging.INFO)


def add(x,y):
    return x+y

def sub(x,y):
    return x-y

def logger(func):
    def log_func(*args):
        logging.info('Running {} with arguments {}'.format(func.__name__, args))
        print(func(*args)) # excecute the function and print results
    return log_func

add_logger = logger(add)
sub_logger = logger(sub)


add_logger(3,3)
add_logger(5,2)
sub_logger(4,3)

'''
Implement the same with a decorator.
'''