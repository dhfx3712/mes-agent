from skill.remind_skill.time_filter_skill import exec as filter

class RemindFilterSub:
    async def filter(self, data, slots):
        res = await filter({"list": data, **slots})
        return {"success": True, "data": res}
