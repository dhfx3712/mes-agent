from common.time_utils import get_today_str
async def exec(p):
    t = get_today_str()
    return [x for x in p["list"] if x.get("remind_time","").startswith(t)]
