'''
When running coroutines, we want to ensure that we don't block. Instead of blocking, we should yield control back to the event loop, so that it can do other tasks. This poses a challenge for most traditional Python libraries that perform IO. Most of these libraries are not designed to be run an event_loop and yield control, instead they block an IO. As a result, in order to perform the functions that these libraries provide, we need to find alternative libraries that support single-threaded asynchronous behavior. Unfortunately everyone's favorite HTTP client requests doesn't have support asyncio; however, there's an alternative library that does, the aiohttp library. The aiohttp library is an HTTP server and client library that was designed for asyncio.
'''
# https://docs.aiohttp.org/en/stable/

from aiohttp import web

'''
implement a http server with aiohttp
'''

async def handle(request):
    name =  request.match_info.get('name','Anonymous')
    text = 'Hello, ' + name
    return web.Response(text=text)

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)

web.run_app(app)
