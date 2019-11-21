import asyncio
import aiohttp
import json
import operator

from datetime import datetime
from fetch import Fetch, BASE_URL, SUFFIX


raw = []
USER_NAME = "whoishiring"
USER_URL = f"""https://hacker-news.firebaseio.com/v0/user/{USER_NAME}.json"""
POST_CHECK_LIM = 50
def get_now():
    now = datetime.now()
    return (now.month, now.year)

async def hit_thread():
    comment_ids = []
    url = USER_URL

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    try:
        comment_ids = data["submitted"]
    except KeyError:
        return None
    return comment_ids


async def collection_helper(session, url):
    async with session.get(url) as response:
        return await response.text()

async def collect_comments(comment_id):
    raw_comments = []
    async with aiohttp.ClientSession() as session:
        data = await collection_helper(
            session, f"{BASE_URL}{comment_id}{SUFFIX}"
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
                    raw.append((title, int(json_data["id"])))


loop = asyncio.get_event_loop()
comment_ids = loop.run_until_complete(hit_thread())

comment_ids = comment_ids[:POST_CHECK_LIM]

loop.run_until_complete(
    asyncio.gather(*[collect_comments(args) for args in comment_ids])
)
raw.sort(key=operator.itemgetter(1), reverse=True)
raw = raw[:12]
for i in raw:
    print (i)