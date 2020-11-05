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
        result = await batch.gather(
            batch.notify("ping"),
            batch.request("plus", 2, 3),
            batch.request("plus", -1, 1),
        )
        print(result)  # [None, Success(result=5, id='2'), Success(result=0, id='3')]


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
