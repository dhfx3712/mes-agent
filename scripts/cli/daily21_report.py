#!/usr/bin/env python3
"""CLI: 21点日报 — 生成并推送日报

Usage:
    scripts/cli/daily21_report.py              # 生成日报（stdout 输出）
    scripts/cli/daily21_report.py --send       # 生成并推送到飞书群

Output (stdout):
    {"status": "success", "data": {"content": "markdown..."}}
    {"status": "error", "error": "..."}
"""
import json
import os
import sys

# Ensure workspace root is on sys.path
_ws_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ws_root not in sys.path:
    sys.path.insert(0, _ws_root)

from common.storage import get_today_stat
from common.config import get, get_feishu_credentials


def _assemble(data):
    """Format rich daily report (was DailyAssembleSub)"""
    date = data.get("date", "")
    summary = data.get("summary", {})
    today_due = data.get("today_due", [])
    upcoming = data.get("upcoming", [])
    completed = data.get("completed", [])
    by_user = data.get("grouped_by_user", {})

    lines = []
    lines.append(f"📋 **21点日报 | {date}**")
    lines.append("")

    # Summary
    lines.append("📊 **总览**")
    stats = []
    if summary.get("today_due"):
        stats.append(f"今日到期：**{summary['today_due']}条**")
    if summary.get("upcoming"):
        stats.append(f"即将到期：**{summary['upcoming']}条**")
    if summary.get("completed_today"):
        stats.append(f"今日完成：**{summary['completed_today']}件**")
    stats.append(f"未完成总计：**{summary.get('total_uncompleted', 0)}条**")
    for s in stats:
        lines.append(f"- {s}")
    lines.append("")

    # Today due
    if today_due:
        lines.append("🔴 **今日到期 ⚠️**")
        for t in today_due:
            p = "🔴P0" if "P0" in (t.get("priority") or "") else "🟡P1"
            lines.append(f"1. **{t['title']}** → {t['user']} | {p}")
        lines.append("")

    # Upcoming
    if upcoming:
        lines.append("📅 **即将到期**")
        for t in upcoming[:10]:
            p = "🔴P0" if "P0" in (t.get("priority") or "") else "🟡P1"
            lines.append(f"- **{t['title']}** → {t['user']} | {p} | 还有{t['days_until']}天")
        if len(upcoming) > 10:
            lines.append(f"- ...还有 {len(upcoming) - 10} 条")
        lines.append("")

    # By user
    if by_user:
        lines.append("👤 **按负责人统计**")
        for name, v in sorted(by_user.items(), key=lambda x: -x[1].get("pending", 0)):
            parts = []
            if v["pending"]:
                parts.append(f"待办{v['pending']}条")
            if v["high_priority"]:
                parts.append(f"高优{v['high_priority']}条")
            lines.append(f"- {name}：{'，'.join(parts)}")
        lines.append("")

    # Completed
    if completed:
        lines.append("✅ **近期完成**")
        for t in completed:
            lines.append(f"- {t['title']} ✅{'（' + t['user'] + '）' if t.get('user') else ''}")
        lines.append("")

    lines.append("💡 **建议：** 请尽快处理高优和今日到期的任务，定期清理延期任务。")

    return "\n".join(lines)


async def main():
    # Fetch + calc (was DailyStatSub)
    raw = await get_today_stat()

    # Assemble (was DailyAssembleSub)
    content = _assemble(raw)

    do_send = "--send" in sys.argv

    if do_send:
        ok = await _send_report(content)
        if not ok:
            print(json.dumps({"status": "error", "error": "日报推送失败"}))
            return

    print(json.dumps({
        "status": "success",
        "data": {"content": content}
    }, ensure_ascii=False))


async def _send_report(content):
    """Send daily report to 工单系统 group chat"""
    import requests

    TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    MSG_URL = "https://open.feishu.cn/open-apis/im/v1/messages"

    app_id, app_secret = get_feishu_credentials("messaging")
    resp = requests.post(TOKEN_URL, json={"app_id": app_id, "app_secret": app_secret})
    token = resp.json()["tenant_access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    chat_id = get("feishu.chat_id")
    payload = {
        "receive_id": chat_id,
        "msg_type": "post",
        "content": json.dumps({
            "zh_cn": {
                "title": "📋 21点日报",
                "content": [[{"tag": "text", "text": content}]]
            }
        })
    }

    resp = requests.post(f"{MSG_URL}?receive_id_type=chat_id", headers=headers, json=payload)
    result = resp.json()
    if result.get("code") != 0:
        print(f"[日报推送失败] {result}")
        return False

    print(f"[日报推送成功] message_id={result.get('data', {}).get('message_id')}")
    return True


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
