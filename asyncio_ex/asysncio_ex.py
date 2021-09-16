import asyncio

# Coroutine function
async def delayedHW():
    print("Hello")
    await asyncio.sleep(2)
    print("Delayed World")


loop = asyncio.get_event_loop()
loop.run_until_complete(delayedHW())
loop.close()


'''
Executing a coroutine function doesn't result in the execution of the
instructions within the function block, rather executing a coroutine function returns something called a coroutine object.

To execute the coroutine object, you need to wrap it in a future object, and pass it to a running event_loop.
In our example, we are not explicitly wrapping the coroutine,
but internally the event_loops run_until_complete method will notice that it's receiving a coroutine object
and not a future object and will wrap it for us.
'''
