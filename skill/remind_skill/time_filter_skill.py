from datetime import datetime

async def exec(p):
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    result = []
    for item in p["list"]:
        remind = item.get("remind_time")
        if remind is None:
            continue
        # Date string format
        if isinstance(remind, str):
            if remind.startswith(today_str):
                result.append(item)
        # Timestamp (ms) - convert to date string
        elif isinstance(remind, (int, float)):
            dt = datetime.fromtimestamp(remind / 1000)
            if dt.strftime("%Y-%m-%d") == today_str:
                result.append(item)
    return result
