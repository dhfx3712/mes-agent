class DailyAssembleSub:
    async def assemble(self, data):
        content = f"""【21点日报】
今日待办：{data['todo_cnt']}
今日提醒：{data['remind_cnt']}"""
        return {"success": True, "data": content}
