import asyncio
from typing import Any, Dict, List, Optional, Union

from aiohttp import web


class Application:
    """Web Application Wrapper for JSON-RPC"""

    def __init__(self):
        """Init Empty Server"""
        self.app = web.Application()
        self.methods = {}

    def method(self, func):
        """Add Method for RPC"""
        self.methods[func.__name__] = func

    async def call(self, method: str, params: Union[List[Any], Dict[str, Any]]) -> Any:
        """Call a method with params"""
        if isinstance(params, list):
            return await self.methods[method](*params)
        elif isinstance(params, dict):
            return await self.methods[method](**params)
        else:
            return None

    async def _process_single(self, data: dict) -> Optional[dict]:
        """Single request/notify

        Parameters
        ----------
        data
            Single JSON Object for Request/Notify

        Returns
        -------
        Result JSON Object for Request,
        or None for Notify
        """
        assert data.get("jsonrpc") == "2.0", "Suppoting Only JSON-RPC 2.0"
        method = data.get("method")
        params = data.get("params", [])
        request_id = data.get("id", None)
        result = await self.call(method, params)

        if request_id is None:  # notify
            return None
        else:  # request
            return {"jsonrpc": "2.0", "result": result, "id": request_id}

    async def _process_batch(self, data: List[dict]) -> List[dict]:
        """Batch of request/notify"""
        return [
            result
            for result in await asyncio.gather(*(self._process_single(o) for o in data))
            if result is not None
        ]

    async def handle(self, request):
        """Web Handler"""
        data = await request.json()

        # single mode
        if isinstance(data, dict):
            return web.json_response(await self._process_single(data))

        # batch mode
        elif isinstance(data, list):
            return web.json_response(await self._process_batch(data))

    def run(
        self,
        port: int = 80,
        endpoint: str = "/",
        host: str = "127.0.0.1",
        debug: bool = False,
    ):
        """Launch a Web Server"""
        self.app.add_routes([web.post(endpoint, self.handle)])
        web.run_app(self.app, host=host, port=port)
