import asyncio

async def get_item(i):
    await asyncio.sleep(1)
    return 'item' + str(i)

async def get_items(num_items):
    print('getting items')
    items_cors = [
    get_item(i)
    for i in range(num_items)
    ]
    print('waiting for tasks to complete')
    # if you have multiple coroutines or tasks,
    # and you want to wait for them all to complete, you can use the asyncio wait function.
    completed, pending = await asyncio.wait(items_cors)
    ## Here we have the get_items coroutine, which executes four get_item coroutine calls
    # in a loop and waits for them all to complete.
    # Because we don't have a timeout and the return_when is defaulted to all_completed,
    # the coroutine will only resume when all the tasks are completed, and the pending set will be empty, so we can just ignore it. 
    results = [t.result() for t in completed]
    print('results:{!r}'.format(results))

loop =  asyncio.get_event_loop()
try:
    loop.run_until_complete(get_items(4))
finally:
    loop.close()
