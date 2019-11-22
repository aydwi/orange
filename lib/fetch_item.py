#!/usr/bin/env python3

import aiohttp
import asyncio
import aiofiles
import json


BASE_URL = "https://hacker-news.firebaseio.com/v0/"
RESOURCE = "item/"
SUFFIX = ".json"


class FetchItem:
    def __init__(self, item_id):
        self.item_id = item_id
        self.raw_comments = []

    async def hit_thread(self):
        comment_ids = []
        url = f"{BASE_URL}{RESOURCE}{self.item_id}{SUFFIX}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
        try:
            comment_ids = data["kids"]
        except KeyError:
            return None
        return comment_ids

    async def collection_helper(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def collect_comments(self, comment_id):
        async with aiohttp.ClientSession() as session:
            data = await self.collection_helper(
                session, f"{BASE_URL}{RESOURCE}{comment_id}{SUFFIX}"
            )
            try:
                json_data = json.loads(data)
            except Exception:
                pass
            self.raw_comments.append(json_data)

"""
if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    f = FetchItem("21419536")

    comment_ids = loop.run_until_complete(f.hit_thread())
    loop.run_until_complete(
        asyncio.gather(*[f.collect_comments(args) for args in comment_ids])
    )
"""