from typing import Any, Dict, List, Union

from aiohttp import web


class Application:
    def __init__(self):
        self.app = web.Application()
        self.methods = {}

    def method(self, func):
        self.methods[func.__name__] = func

    async def process(
        self, method: str, params: Union[List[Any], Dict[str, Any]]
    ) -> Any:
        if isinstance(params, list):
            print(method, params)
            return await self.methods[method](*params)
        elif isinstance(params, dict):
            return await self.methods[method](**params)
        else:
            return None

    async def handle(self, request):
        # TODO: Error Handling
        data = await request.json()
        print(data)
        print(data.get("jsonrpc"))
        assert data.get("jsonrpc") == "2.0", "Suppoting Only JSON-RPC 2.0"
        method = data.get("method")
        params = data.get("params", [])
        result = await self.process(method, params)
        request_id = data.get("id", None)
        return web.json_response(
            {"jsonrpc": "2.0", "result": result, "id": request_id,}
        )

    def run(
        self,
        port: int = 80,
        endpoint: str = "/",
        host: str = "127.0.0.1",
        debug: bool = False,
    ):
        self.app.add_routes([web.post(endpoint, self.handle)])
        web.run_app(self.app, host=host, port=port)
