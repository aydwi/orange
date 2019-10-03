#!/usr/bin/env python3

import aiohttp
import asyncio
import aiofiles
import requests
import json

from multiprocessing import Pool


BASE_URL = """https://hacker-news.firebaseio.com/v0/item/"""
SUFFIX = """.json?print=pretty"""


def aget(k):
    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def main(id):
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, BASE_URL + str(id) + SUFFIX)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*[main(args) for args in k]))


def pool_handler():
    p = Pool(8)
    p.map(aget, sublists)


if __name__ == "__main__":

    r = requests.get(
        url="https://hacker-news.firebaseio.com/v0/item/19543940.json?print=pretty"
    )
    k = r.json()["kids"]

    sublists = [k[x : x + 300] for x in range(0, len(k), 300)]

    pool_handler()
    # aget(k)
