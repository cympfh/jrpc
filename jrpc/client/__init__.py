from typing import Any, Dict, List

import aiohttp

from jrpc.client import result


class Client:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    async def request(
        self, method: str, *list_params: List[Any], **kw_params: Dict[str, Any]
    ) -> result.Result:
        async with aiohttp.ClientSession() as session:
            request_json = {
                "jsonrpc": "2.0",
                "method": method,
                "id": "42",
            }
            if len(kw_params) == 0:
                request_json["params"] = list_params
            else:
                request_json["params"] = kw_params
            async with session.post(self.endpoint, json=request_json) as response:
                response_json = await response.json()
                return result.from_json(response_json)
