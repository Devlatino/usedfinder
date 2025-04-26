
import os, json, asyncio, asyncpg, rq, redis
from common.schemas import Listing

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
rconn = redis.from_url(REDIS_URL)
queue = rq.Queue("listings", connection=rconn)

TRIGRAM_SQL = """
SELECT id
FROM saved_search
WHERE title % $1 OR similarity(title, $1) > 0.3
"""

async def match_listing(conn, listing: Listing):
    rows = await conn.fetch(TRIGRAM_SQL, listing.title)
    for row in rows:
        await conn.execute(
            """INSERT INTO notification(user_id, item_id)
               VALUES ($1,$2) ON CONFLICT DO NOTHING""",
            row["id"], listing.item_id
        )

async def worker():
    pool = await asyncpg.create_pool(dsn=os.getenv("PG_DSN"))
    while True:
        job = queue.dequeue(timeout=5)
        if job:
            listing = Listing(**json.loads(job.args[0]))
            async with pool.acquire() as conn:
                await match_listing(conn, listing)
        else:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(worker())
