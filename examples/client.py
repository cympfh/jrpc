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
