from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

import aiohttp
import aiohttp.web

from jrpc.client import result


@dataclass
class Request:
    """Send Type"""

    method: str
    params: Union[List[Any], Dict[str, Any]]
    id: str

    def to_json(self) -> dict:
        return {
            "jsonrpc": "2.0",
            "method": self.method,
            "params": self.params,
            "id": self.id,
        }


@dataclass
class Notify:
    """Send Type"""

    method: str
    params: Union[List[Any], Dict[str, Any]]

    def to_json(self) -> dict:
        return {
            "jsonrpc": "2.0",
            "method": self.method,
            "params": self.params,
        }


Request_T = Union[Request, Notify]


class Client:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.time = 0

    def id_generate(self) -> str:
        """Returns Request-Id"""
        self.time += 1
        return str(self.time)

    @asynccontextmanager
    async def _send(self, req: Request_T) -> aiohttp.web.Response:
        async with aiohttp.ClientSession() as session:
            request_json = req.to_json()
            async with session.post(self.endpoint, json=request_json) as response:
                yield response

    async def request(
        self, method: str, *list_params: Tuple[Any], **kw_params: Dict[str, Any]
    ) -> result.Result:
        """Send and Returns Result"""
        req = Request(method, list(list_params) or dict(kw_params), self.id_generate())
        async with self._send(req) as response:
            response_json = await response.json()
            return result.from_json(response_json)

    async def notify(
        self, method: str, *list_params: Tuple[Any], **kw_params: Dict[str, Any]
    ):
        """Send and Returns None"""
        req = Notify(method, list(list_params) or dict(kw_params))
        async with self._send(req):
            return

    @contextmanager
    def batch(self):
        """Enter Batch Mode"""
        yield BatchClient(self)


class BatchClient:
    """Batch Mode"""

    def __init__(self, client: Client):
        self.client = client
        self.time = 0
        self.ids = []
        self.result = {}

    def id_generate(self) -> str:
        """Returns Request-Id"""
        self.time += 1
        request_id = str(self.time)
        self.ids.append(request_id)
        self.result[request_id] = None
        return request_id

    async def gather(self, *requests: List[Request_T]) -> List[result.Result]:
        request_json = [req.to_json() for req in requests]
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.client.endpoint, json=request_json
            ) as response:
                response_json = await response.json()
                for o in response_json:
                    res = result.from_json(o)
                    self.result[res.id] = res

                return [self.result[id] for id in self.ids]

    def request(self, method: str, *list_params, **kw_params) -> Request:
        request_id = self.id_generate()
        return Request(method, list(list_params) or dict(kw_params), request_id)

    def notify(self, method: str, *list_params, **kw_params) -> Notify:
        _ = self.id_generate()
        return Notify(method, list(list_params) or dict(kw_params))
