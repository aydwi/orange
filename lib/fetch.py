#!/usr/bin/env python3

import aiohttp
import asyncio
import aiofiles
import requests
import json
import urwid
import random

from multiprocessing import Pool


BASE_URL = """https://hacker-news.firebaseio.com/v0/item/"""
SUFFIX = """.json?print=pretty"""


class Fetch:
    def __init__(self, thread_id):
        self.thread_id = thread_id
        self.raw_comments = []

    async def hit_thread(self):
        comment_ids = []
        url = f"{BASE_URL}{self.thread_id}{SUFFIX}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
        try:
            comment_ids = data["kids"]
        except KeyError:
            return None
        return comment_ids

    async def fetch_response(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def main(self, comment_id):
        async with aiohttp.ClientSession() as session:
            raw_data = await self.fetch_response(
                session, f"{BASE_URL}{comment_id}{SUFFIX}"
            )
            data = json.loads(raw_data)
            try:
                self.raw_comments.append(repr(data["text"]))
            except:
                pass


loop = asyncio.get_event_loop()

o = Fetch("21419536")
k = loop.run_until_complete(o.hit_thread())
loop.run_until_complete(asyncio.gather(*[o.main(args) for args in k]))
