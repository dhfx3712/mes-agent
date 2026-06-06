from common.storage import get_user_remind
async def exec(p):
    return await get_user_remind(p["user_id"], p.get("days",1))
