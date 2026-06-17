"""Agent ↔ Flow 桥接脚本

Usage:
    python3 run_flow.py <flow_name> '<slots_json>' '<ctx_json>'

Flows:
    todo_create  - 新增待办
    remind_query - 查询提醒
    daily21      - 21点日报
"""
import sys, json, asyncio


async def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "msg": "Usage: run_flow.py <flow_name> [slots_json] [ctx_json]"}))
        return

    flow_name = sys.argv[1]
    slots = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    ctx = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}

    if flow_name == "todo_create":
        from flow.todo_create_flow.flow_run import run_flow
        result = await run_flow(slots, ctx)
    elif flow_name == "remind_query":
        from flow.remind_query_flow.flow_run import run_flow
        result = await run_flow(slots, ctx)
    elif flow_name == "daily21":
        from flow.daily21_report_flow.flow_run import run_flow
        result = await run_flow()
    else:
        result = {"success": False, "msg": f"Unknown flow: {flow_name}"}

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
