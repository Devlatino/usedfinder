
import abc
from typing import AsyncIterator, Dict, Any

class BaseCrawler(abc.ABC):
    marketplace: str

    @abc.abstractmethod
    async def search(
        self, query: str, **kwargs
    ) -> AsyncIterator[Dict[str, Any]]:
        """Return async iterator of listings"""
