
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import os, redis, rq, json, asyncio

from crawler.subito import SubitoCrawler
from crawler.ebay import EbayCrawler
from common.schemas import Listing

app = FastAPI()
rconn = redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))
queue = rq.Queue("listings", connection=rconn)

class SearchIn(BaseModel):
    term: str

async def run_crawlers(term: str):
    async for item in SubitoCrawler().search(term):
        queue.enqueue(json.dumps(item | {"marketplace": "subito"}))
    async for item in EbayCrawler().search(term):
        queue.enqueue(json.dumps(item | {"marketplace": "ebay"}))

@app.post("/search")
async def search(s: SearchIn, bg: BackgroundTasks):
    bg.add_task(run_crawlers, s.term)
    return {"status": "started"}
