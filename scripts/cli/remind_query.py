#!/usr/bin/env python3
"""CLI: 查询提醒

Usage:
    scripts/cli/remind_query.py '<slots_json>' '<ctx_json>'

Args:
    slots: {"days": 1}
    ctx:   {"user_id": "ou_xxx"}

Output (stdout):
    {"status": "success", "data": [{"title": "...", "deadline": "...", ...}]}
    {"status": "error", "error": "..."}
"""
import json
import os
import sys
from datetime import datetime

# Ensure workspace root is on sys.path
_ws_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ws_root not in sys.path:
    sys.path.insert(0, _ws_root)

from common.storage import get_user_remind


async def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "error": "Missing slots JSON"}))
        return

    slots = json.loads(sys.argv[1])
    ctx = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    user_id = ctx.get("user_id", "")
    days = slots.get("days", 1)

    # Query (was RemindQuerySub)
    data = await get_user_remind(user_id, days)

    # Filter by today (was RemindFilterSub / time_filter_skill)
    today_str = datetime.now().strftime("%Y-%m-%d")
    filtered = []
    for item in data:
        remind = item.get("remind_time")
        if remind is None:
            continue
        if isinstance(remind, str):
            if remind.startswith(today_str):
                filtered.append(item)
        elif isinstance(remind, (int, float)):
            dt = datetime.fromtimestamp(remind / 1000)
            if dt.strftime("%Y-%m-%d") == today_str:
                filtered.append(item)

    print(json.dumps({
        "status": "success",
        "data": filtered
    }, ensure_ascii=False))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
