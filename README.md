# jrpc

JSON-RPC 2.0 Implementation for Python 3.7+.

## This Repository is...

Just Experimental.

- [x] request
- [ ] batch request
- [x] notify
- [ ] Error handling

## What is JSON-RPC?

You can see the Spec [here](https://www.jsonrpc.org/specification).
It's very Easy!

## Example?

### Server Code

```python
from jrpc.server import Application

app = Application()


@app.method
async def ping() -> str:
    """ping method"""
    return "pong"


@app.method
async def plus(n: int, m: int) -> int:
    """Addition"""
    return n + m


app.run(host="0.0.0.0", endpoint="/", port=8080, debug=True)
```

### Request by curl

```bash
$ curl -X POST localhost:8080 --data '{"jsonrpc":"2.0", "method":"ping"}'
{"jsonrpc": "2.0", "result": "pong", "id": null}

$ curl -X POST localhost:8080 --data '{"jsonrpc":"2.0", "method":"plus", "params":[2, 3], "id":"fuga"}'
{"jsonrpc": "2.0", "result": 5, "id": "fuga"}
```

### Client Code

```python
import asyncio

from jrpc.client import Client


async def main():
    client = Client(endpoint="http://localhost:8080/")

    response = await client.request("ping")
    print(response)

    response = await client.request("plus", 2, 3)
    print(response)

    response = await client.request("plus", n=2, m=3)
    print(response)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
