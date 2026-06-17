from agent.sub_agent.remind_sub.remind_query_sub import RemindQuerySub
from agent.sub_agent.remind_sub.remind_filter_sub import RemindFilterSub

class RemindMainAgent:
    async def run(self, slots: dict, ctx: dict):
        data = await RemindQuerySub().query(slots, ctx)
        return await RemindFilterSub().filter(data["data"], slots)
