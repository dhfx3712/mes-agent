from skill.daily21_skill.data_fetch_skill import exec as fetch
from skill.daily21_skill.calc_skill import exec as calc

class DailyStatSub:
    async def stat(self):
        raw = await fetch()
        return {"success": True, "data": await calc(raw)}
