#!/usr/bin/env python3
"""CLI: 新增待办

Usage:
    scripts/cli/todo_create.py '<slots_json>' '<ctx_json>'

Args:
    slots: {"title": "...", "time": "2026-06-17", "content": "...", "priority": "🔴P0"}
    ctx:   {"user_id": "ou_xxx"}

Output (stdout):
    {"status": "success", "data": {"record_id": "recXXX"}}
    {"status": "error", "error": "..."}
"""
import json
import os
import sys

# Ensure workspace root is on sys.path
_ws_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ws_root not in sys.path:
    sys.path.insert(0, _ws_root)

from common.storage import save_todo


async def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "error": "Missing slots JSON"}))
        return

    slots = json.loads(sys.argv[1])
    ctx = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    # Param check (was TodoParamCheckSub)
    title = slots.get("title", "")
    if not title:
        print(json.dumps({"status": "error", "error": "请输入待办标题"}))
        return

    # Save (was TodoCreateSub)
    user_id = ctx.get("user_id", "")
    record_id = await save_todo(user_id, slots)

    print(json.dumps({
        "status": "success",
        "data": {"record_id": record_id}
    }, ensure_ascii=False))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
