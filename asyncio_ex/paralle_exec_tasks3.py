import asyncio
import itertools

'''
The as_completed method also lets you specify an optional timeout value. If a timeout occurs before all the tasks are done, then a timeout error is raised. With both the wait and the as_completed methods, the return value is a collection of futures. The asyncio. gather method differs in this regard. Instead of returning a collection of futures, the gather method returns a single future that aggregates the result from the past and futures. The results are aggregated in order of the original sequence, not necessarily in order of the results or rival, which is highly beneficial in cases where a business logic requires it.
'''

async def get_item(i):
    print('getting items')
    await asyncio.sleep(i)
    return 'item' + str(i)

async def get_items(num_items):
    print('getting items')
    items_cors = [
    get_item(i)
    for i in range(num_items)
    ]

    # if you have multiple coroutines or tasks
    # Note the use of splat operator on the item_coros list to
    # unpack the list into positional arguments for the gather function.
    results = await asyncio.gather(*items_cors)
    print(type(results))
    data = list(itertools.chain.from_iterable(results))
    print(type(data))
    print('results:{!r}'.format(results))
    print('data:{!r}'.format(data))
    ## Here we have the get_items coroutine, which executes four get_item coroutine calls
    # in a loop and waits for them all to complete.


loop =  asyncio.get_event_loop()
try:
    loop.run_until_complete(get_items(3))
finally:
    loop.close()
