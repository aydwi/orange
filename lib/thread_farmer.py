import asyncio
import aiohttp
import json
import operator

from datetime import datetime


BASE_URL = "https://hacker-news.firebaseio.com/v0/"
RESOURCE = "user/"
USER_NAME = "whoishiring"
SUFFIX = ".json"

POST_CHECK_LIM = 50


class ThreadFarmer:
    def __init__(self):
        self.thread_farm = []

    async def hit_user(self):
        post_ids = []
        url = f"{BASE_URL}{RESOURCE}{USER_NAME}{SUFFIX}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
        try:
            post_ids = data["submitted"]
        except KeyError:
            return None
        return post_ids

    async def collection_helper(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def collect_titles(self, post_id):
        async with aiohttp.ClientSession() as session:
            data = await self.collection_helper(
                session, f"{BASE_URL}item/{post_id}{SUFFIX}"
            )
            json_data = json.loads(data)
            try:
                dead = json_data["dead"]
            except KeyError:
                try:
                    title = json_data["title"]
                except KeyError:
                    pass
                else:
                    if title.startswith("Ask HN: Who is hiring?"):
                        self.thread_farm.append((title, int(json_data["id"])))


if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    t = ThreadFarmer()

    post_ids = loop.run_until_complete(t.hit_user())
    post_ids = post_ids[:POST_CHECK_LIM]

    loop.run_until_complete(
        asyncio.gather(*[t.collect_titles(args) for args in post_ids])
    )
    thread_farm = t.thread_farm
    thread_farm.sort(key=operator.itemgetter(1), reverse=True)
    thread_farm = thread_farm[:12]

    for i in thread_farm:
        print(i)
