# https://julien.danjou.info/python-tenacity/
import tenacity

'''
@tenacity.retry
@tenacity.retry(wait=tenacity.wait_fixed(1))
@tenacity.retry(wait=tenacity.wait_exponential())
@tenacity.retry(wait=tenacity.wait_fixed(10) + wait.wait_random(0, 3))

What is especially interesting with tenacity, is that you can easily combine several methods. For example, you can combine tenacity.wait.wait_random with tenacity.wait.wait_fixed to wait a number of seconds defined in an interval:
Above will make the function being retried wait randomly between 10 and 13 seconds before trying again.

tenacity offers more customization, such as retrying on some exceptions only. You can retry every second to execute the function only if the exception raised
@tenacity.retry(wait=tenacity.wait_fixed(1),
                retry=tenacity.retry_if_exception_type(IOError))

You can combine several condition easily by using the | or & binary operators.
They are used to make the code retry if an IOError exception is raised, or if no result is returned.
Also, a stop condition is added with the stop keyword arguments.
It allows to specify a condition unrelated to the function result of exception to stop, such as a number of attemps or a delay.

@tenacity.retry(wait=tenacity.wait_fixed(1),
                stop=tenacity.stop_after_delay(60),
                retry=(tenacity.retry_if_exception_type(IOError) |
                       tenacity.retry_if_result(lambda result: result == None))

The function can raise `tenacity.TryAgain` at any time if the function decides that it's better to retry.

'''
