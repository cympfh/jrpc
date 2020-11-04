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
