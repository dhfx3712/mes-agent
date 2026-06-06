import json
import requests
from datetime import datetime, timezone

BASE = "IR19b1JZJa1shNsA9zCc3QIMnEh"
TABLE = "tbljSyRPEgXmWUYF"
CONFIG_PATH = "/root/.openclaw/openclaw.json"
TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
API_URL = "https://open.feishu.cn/open-apis/bitable/v1/apps"


def _get_credentials():
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    for acct in cfg["channels"]["feishu"]["accounts"]:
        if acct.get("appId") == "cli_a95451a74db8dcd2":
            return acct["appId"], acct["appSecret"]
    raise RuntimeError("Feishu credentials not found in config")


def _get_token():
    app_id, app_secret = _get_credentials()
    resp = requests.post(TOKEN_URL, json={
        "app_id": app_id,
        "app_secret": app_secret
    })
    return resp.json()["tenant_access_token"]


def _headers():
    return {"Authorization": f"Bearer {_get_token()}"}


def _fetch_all_records():
    """Fetch up to 1000 records (no filter, all fields returned)"""
    resp = requests.get(
        f"{API_URL}/{BASE}/tables/{TABLE}/records",
        headers=_headers(),
        params={"page_size": 500}
    )
    data = resp.json()
    items = data.get("data", {}).get("items", [])

    # Handle pagination
    page_token = data.get("data", {}).get("page_token")
    while page_token:
        resp = requests.get(
            f"{API_URL}/{BASE}/tables/{TABLE}/records",
            headers=_headers(),
            params={"page_size": 500, "page_token": page_token}
        )
        data = resp.json()
        items.extend(data.get("data", {}).get("items", []))
        page_token = data.get("data", {}).get("page_token")

    return items


def _to_ms_timestamp(date_str):
    """Convert 'YYYY-MM-DD' or 'YYYY/MM/DD' to ms timestamp"""
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            # Use local time (Asia/Shanghai = UTC+8)
            return int(dt.timestamp() * 1000)
        except ValueError:
            continue
    return None


def _get_executor_ids(fields):
    """Extract executor open_ids from fields"""
    executors = fields.get("执行人", []) or []
    return [e.get("id", "") for e in executors]


async def save_todo(user_id, data):
    """Create a new todo record

    Slots: {title, time(optional), content(optional), priority(optional)}
    """
    fields = {"待办事项": data.get("title", "")}

    time_val = data.get("time")
    if time_val:
        ts = _to_ms_timestamp(time_val)
        if ts:
            fields["截止日期"] = ts

    content_val = data.get("content")
    if content_val:
        fields["AI 待办事项汇总"] = content_val

    priority = data.get("priority")
    if priority:
        fields["优先级"] = priority

    if user_id and user_id.startswith("ou_"):
        fields["执行人"] = [{"id": user_id}]

    resp = requests.post(
        f"{API_URL}/{BASE}/tables/{TABLE}/records",
        headers=_headers(),
        json={"fields": fields}
    )
    result = resp.json()
    if result.get("code") != 0:
        raise RuntimeError(f"Feishu API error: {result}")
    return result.get("data", {}).get("record", {}).get("record_id")


async def get_user_remind(user_id, days=1):
    """Get recent reminders for a user"""
    items = _fetch_all_records()
    now = datetime.now()

    result_list = []
    for item in items:
        fields = item.get("fields", {})

        # Filter by user
        executor_ids = _get_executor_ids(fields)
        if user_id not in executor_ids:
            continue

        # Filter by creation time (within N days)
        created = fields.get("创建时间")
        if created:
            created_dt = datetime.fromtimestamp(created / 1000)
            if (now - created_dt).days > days:
                continue

        result_list.append({
            "title": fields.get("待办事项", ""),
            "remind_time": fields.get("截止日期"),
            "record_id": item.get("record_id"),
            "completed": fields.get("是否已完成", False),
            "priority": fields.get("优先级"),
        })

    return result_list


async def list_uncompleted(user_id=None):
    """List uncompleted todos, optionally filtered by user"""
    items = _fetch_all_records()
    now_ms = datetime.now().timestamp() * 1000

    result_list = []
    for item in items:
        fields = item.get("fields", {})

        # Skip completed
        if fields.get("是否已完成", False):
            continue

        # Filter by user if specified
        if user_id:
            executor_ids = _get_executor_ids(fields)
            if user_id not in executor_ids:
                continue

        deadline = fields.get("截止日期")
        deadline_passed = deadline is not None and deadline < now_ms

        result_list.append({
            "record_id": item.get("record_id"),
            "title": fields.get("待办事项", ""),
            "deadline": deadline,
            "priority": fields.get("优先级"),
            "executor": fields.get("执行人"),
            "deadline_passed": deadline_passed,
            "distance": fields.get("距离截止日"),
        })

    return result_list


async def get_today_stat():
    """Get today's statistics"""
    items = _fetch_all_records()
    today = datetime.now().strftime("%Y-%m-%d")
    today_start = _to_ms_timestamp(today)
    today_end = today_start + 86400000 if today_start else 0

    today_items = [
        item for item in items
        if today_start <= (item.get("fields", {}).get("创建时间") or 0) < today_end
    ]

    return {
        "todo_cnt": len(today_items),
        "remind_cnt": len(today_items),
        "date": today
    }
