# jrpc

JSON-RPC 2.0 Implementation for Python 3.7+.

## This Repository is...

Just Experimental.

- [x] request
- [x] batch request
- [x] notify
- [ ] Error handling
- [ ] logging
- [ ] debug mode

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
# request "ping"
$ curl -X POST localhost:8080 --data '{"jsonrpc":"2.0", "method":"ping", "id":"42"}'
{"jsonrpc": "2.0", "result": "pong", "id": "42"}

# notify "ping" (without id)
$ curl -X POST localhost:8080 --data '{"jsonrpc":"2.0","method":"ping"}'
null

# request "plus" with params
$ curl -X POST localhost:8080 --data '{"jsonrpc":"2.0", "method":"plus", "params":[2, 3], "id":"fuga"}'
{"jsonrpc": "2.0", "result": 5, "id": "fuga"}

# request/notify by batch
$ curl -X POST localhost:8080 --data '[{"jsonrpc":"2.0","method":"ping"},{"id":"calc1","jsonrpc":"2.0","method":"plus","params":[2,3]},{"id":"calc2","jsonrpc":"2.0","method":"plus","params":[1,-1]}]'
[{"jsonrpc": "2.0", "result": 5, "id": "calc1"}, {"jsonrpc": "2.0", "result": 0, "id": "calc2"}]%
```

### Client Code

```python
import asyncio

from jrpc.client import Client


async def main():
    client = Client(endpoint="http://localhost:8080/")

    response = await client.request("ping")
    print(response)

    response = await client.notify("ping")
    print(response)  # None

    response = await client.request("plus", 2, 3)
    print(response)

    response = await client.request("plus", n=2, m=3)
    print(response)

    with client.batch() as batch:
        result = batch.gather(
            batch.notify("ping"),
            batch.request("plus", 2, 3),
            batch.request("plus", -1, 1),
        )
        print(result)  # [None, Success(result=5, id='2'), Success(result=0, id='3')]


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
