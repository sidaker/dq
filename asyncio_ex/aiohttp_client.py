import aiohttp
import asyncio
import async_timeout

'''
A asynchronous context manager is a context manager that is able to yield control
within its enter and exit methods.

The client session object is the main interface for making HTTP requests,
and it has coroutine methods like get, post, put, and delete that correspond
to the standard HTTP methods.

After creating our session object, we called the fetch coroutine,
passing in the session object and the URL to get.
In our fetch coroutine, we invoke session. get, passing in the URL
and use another asynchronous context manager to manage the response object.
The response to text method is also a coroutine. So we await its completion,
and then return the results to the main coroutine, which prints it. 
'''

async def fetch(session,url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        html =  await fetch(session, 'http://python.org')
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
