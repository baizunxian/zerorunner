from typing import Any

from aiohttp import ClientSession
from aiohttp.typedefs import StrOrURL


class AsyncHttp(ClientSession):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def request(self, method: str, url: StrOrURL, **kwargs: Any):
        resp = await super().request(method, url, **kwargs)
        await self.close()
        return resp
