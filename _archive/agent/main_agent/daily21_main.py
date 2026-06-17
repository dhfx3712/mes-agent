from agent.sub_agent.daily21_sub.daily_stat_sub import DailyStatSub
from agent.sub_agent.daily21_sub.daily_assemble_sub import DailyAssembleSub

class Daily21MainAgent:
    async def run(self):
        stat = await DailyStatSub().stat()
        return await DailyAssembleSub().assemble(stat["data"])
