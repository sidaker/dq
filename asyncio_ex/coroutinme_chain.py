import asyncio

async def perf_task():
    print('Perform Task')
    print('waiting for Result1')
    result1 = await subtask1()
    print('waiting for result2')
    result2 = await subtask2(result1)
    return(result1, result2)

async def subtask1():
    print('perform subtask 1')
    return 'result1'


async def subtask2(arg):
    print('perform subtask 2')
    return f'result2 relies on {arg}'

loop = asyncio.get_event_loop()
result = loop.run_until_complete(perf_task())
loop.close()
