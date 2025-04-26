
import asyncio, re
from typing import AsyncIterator, Dict, Any
from aiohttp import ClientSession, ClientTimeout
from parsel import Selector
from .base import BaseCrawler

URL_SEARCH = "https://www.subito.it/annunci-tutta-italia/?q={term}&o={page}"
PRICE_RE = re.compile(r"([0-9\.\s]+)[^0-9]")

class SubitoCrawler(BaseCrawler):
    marketplace = "subito"

    async def _fetch(self, session: ClientSession, url: str) -> str:
        async with session.get(url, timeout=ClientTimeout(total=15)) as r:
            r.raise_for_status()
            return await r.text()

    async def _parse(self, sel: Selector) -> Dict[str, Any]:
        href = sel.css("a.AdCardLink__Link-sc-1h74x40-0::attr(href)").get()
        if not href:
            return {}
        title = sel.css("h2::text").get(default="").strip()
        price_raw = sel.css("p.Price__StyledPrice-sc-1rah4ud-0::text").get("")
        m = PRICE_RE.search(price_raw or "")
        price = int(m.group(1).replace(".", "").replace(" ", "")) if m else None
        return {
            "item_id": href.split("-")[-1].replace(".htm", ""),
            "title": title,
            "price": price,
            "currency": "EUR",
            "url": f"https://www.subito.it{href}",
        }

    async def search(self, query: str, pages: int = 1) -> AsyncIterator[Dict[str, Any]]:
        async with ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as s:
            for page in range(1, pages + 1):
                url = URL_SEARCH.format(term=query.replace(" ", "+"), page=page)
                html = await self._fetch(s, url)
                for node in Selector(text=html).css("div.items-list > div"):
                    listing = await self._parse(node)
                    if listing:
                        yield listing
