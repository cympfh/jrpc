from contextlib import asynccontextmanager
from typing import Any, Dict, Optional, Tuple

import aiohttp
import aiohttp.web

from jrpc.client import result


class Client:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.time = 0

    def id_generate(self) -> str:
        """Returns Request-Id"""
        self.time += 1
        return str(self.time)

    @asynccontextmanager
    async def _send(
        self,
        method: str,
        request_id: Optional[str],
        *list_params: Tuple[Any],
        **kw_params: Dict[str, Any]
    ) -> aiohttp.web.Response:
        async with aiohttp.ClientSession() as session:
            request_json = {
                "jsonrpc": "2.0",
                "method": method,
            }
            if request_id is not None:
                request_json["id"] = request_id
            request_json["params"] = kw_params if bool(kw_params) else list(list_params)
            async with session.post(self.endpoint, json=request_json) as response:
                yield response

    async def request(
        self, method: str, *list_params: Tuple[Any], **kw_params: Dict[str, Any]
    ) -> result.Result:
        """Send and Returns Result"""
        async with self._send(
            method, self.id_generate(), *list_params, **kw_params
        ) as response:
            response_json = await response.json()
            return result.from_json(response_json)

    async def notify(
        self, method: str, *list_params: Tuple[Any], **kw_params: Dict[str, Any]
    ):
        """Send and Returns None"""
        async with self._send(method, None, *list_params, **kw_params):
            return
