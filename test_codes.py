# import asyncio


# async def delayed_print(text, time=1):
#     await asyncio.sleep(time)
#     print(text)


# async def main_coro():
#     # python >= 3.7
#     task1 = asyncio.create_task(delayed_print("I'm printed second!", 2))
#     # python >= 3.3
#     task2 = asyncio.ensure_future(delayed_print("I'm printed first!"))
#     await asyncio.gather(task1, task2, delayed_print("I'm printed last!", 3))


# # python >= 3.7
# asyncio.run(main_coro())


import aiohttp
import asyncio
from itertools import chain

API_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "user-agent": "ConcurrentSearchBot/0.1 (educational project)",
}

PARAMS = {
    "action": "query",
    "list": "search",
    "srsearch": "biology",
    "srlimit": 1,
    "format": "json",
}


async def fetch(session, url, params):
    async with session.get(url, params=params) as response:

        print(response.status)
        print(response.headers.get("Content-Type"))
        print(response.url)

        return await response.json()


async def fetch_all():
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        task = asyncio.create_task(fetch(session, API_URL, PARAMS))

        response = await task

        print()
        print(f"Название статьи: {response["query"]["search"][0]["title"]}")
        print()
        print("SNIPPET:")
        print(response["query"]["search"][0]["snippet"].strip())
        print()
        for k in response:
            print(response[k])


print(asyncio.run(fetch_all()))
