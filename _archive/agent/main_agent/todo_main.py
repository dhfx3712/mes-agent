from agent.sub_agent.todo_sub.todo_param_check_sub import TodoParamCheckSub
from agent.sub_agent.todo_sub.todo_create_sub import TodoCreateSub

class TodoMainAgent:
    async def run(self, slots: dict, ctx: dict):
        check = await TodoParamCheckSub().check(slots)
        if not check["success"]:
            return check
        return await TodoCreateSub().create(slots, ctx)
