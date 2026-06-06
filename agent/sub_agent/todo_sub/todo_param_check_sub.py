class TodoParamCheckSub:
    async def check(self, slots):
        if not slots.get("title"):
            return {"success": False, "msg": "请输入待办标题"}
        return {"success": True}
