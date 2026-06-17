from common.storage import save_todo
async def exec(params):
    return await save_todo(params["user_id"], params)
