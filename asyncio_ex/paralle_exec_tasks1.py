import asyncio

async def get_item(i):
    print('getting items')
    await asyncio.sleep(1)
    return 'item' + str(i)

async def get_items(num_items):
    print('getting items')
    items_cors = [
    get_item(i)
    for i in range(num_items)
    ]
    print('waiting 2 secs for tasks to complete')
    # if you have multiple coroutines or tasks,
    # and you want to wait for them all to complete, you can use the asyncio wait function.
    completed, pending = await asyncio.wait(items_cors, timeout=2)
    results = [t.result() for t in completed]
    print('results:{!r}'.format(results))
    ## Here we have the get_items coroutine, which executes four get_item coroutine calls
    # in a loop and waits for them all to complete.
    if pending:
        print('cancelling remaing tasks')
        for t in pending:
            t.cancel()

loop =  asyncio.get_event_loop()
try:
    loop.run_until_complete(get_items(6))
finally:
    loop.close()
