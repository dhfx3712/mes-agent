from skill.todo_skill.save_todo_skill import exec as save

class TodoCreateSub:
    async def create(self, slots, ctx):
        res = await save({"user_id": ctx.get("user_id"), **slots})
        return {"success": True, "msg": "已写入飞书表格", "data": res}
