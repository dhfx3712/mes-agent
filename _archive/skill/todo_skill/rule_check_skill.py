async def exec(params):
    return len(params.get("title", "")) <= 100
