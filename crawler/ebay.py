
from typing import AsyncIterator, Dict, Any
from ebay_rest import API
from .base import BaseCrawler
import os, asyncio

class EbayCrawler(BaseCrawler):
    marketplace = "ebay"

    def __init__(self, app_id: str | None = None, cert_id: str | None = None):
        self.api = API(
            app_id or os.getenv("EBAY_APP_ID"),
            cert_id or os.getenv("EBAY_CERT_ID"),
            site_id="EBAY_IT"
        )

    async def search(self, query: str, pages: int = 1) -> AsyncIterator[Dict[str, Any]]:
        async with self.api:
            for p in range(pages):
                resp = await self.api.buy.browse.search(
                    q=query,
                    limit=50,
                    offset=p * 50,
                    filter="itemLocationCountry:IT"
                )
                for it in resp.get("itemSummaries", []):
                    yield {
                        "item_id": it["itemId"],
                        "title": it["title"],
                        "price": int(float(it["price"]["value"])),
                        "currency": it["price"]["currency"],
                        "url": it["itemWebUrl"],
                    }
