from skill.remind_skill.db_query_skill import exec as query

class RemindQuerySub:
    async def query(self, slots, ctx):
        data = await query({"user_id": ctx.get("user_id"), **slots})
        return {"success": True, "data": data}
