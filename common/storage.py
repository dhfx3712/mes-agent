import requests
from datetime import datetime, timezone, timedelta

from common.config import get, get_feishu_credentials

# Asia/Shanghai timezone (UTC+8)
_TZ_SHANGHAI = timezone(timedelta(hours=8))

TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
API_URL = "https://open.feishu.cn/open-apis/bitable/v1/apps"


def _get_token():
    app_id, app_secret = get_feishu_credentials("bitable")
    resp = requests.post(TOKEN_URL, json={
        "app_id": app_id,
        "app_secret": app_secret
    })
    return resp.json()["tenant_access_token"]


def _headers():
    return {"Authorization": f"Bearer {_get_token()}"}


def _fetch_quick_query_records():
    """Fetch records filtered by quick query view (used by list_uncompleted)"""
    base = get("bitable.base_app_id")
    table = get("bitable.table_id")
    view_id = get("bitable.quick_query_view_id")
    params = {"page_size": 500}
    if view_id:
        params["view_id"] = view_id
    resp = requests.get(
        f"{API_URL}/{base}/tables/{table}/records",
        headers=_headers(),
        params=params
    )
    data = resp.json()
    items = data.get("data", {}).get("items", [])

    page_token = data.get("data", {}).get("page_token")
    while page_token:
        params["page_token"] = page_token
        resp = requests.get(
            f"{API_URL}/{base}/tables/{table}/records",
            headers=_headers(),
            params=params
        )
        data = resp.json()
        items.extend(data.get("data", {}).get("items", []))
        page_token = data.get("data", {}).get("page_token")

    return items


def _fetch_view_records():
    """Fetch records filtered by configured view (used by daily report)"""
    base = get("bitable.base_app_id")
    table = get("bitable.table_id")
    view_id = get("bitable.view_id")
    params = {"page_size": 500}
    if view_id:
        params["view_id"] = view_id
    resp = requests.get(
        f"{API_URL}/{base}/tables/{table}/records",
        headers=_headers(),
        params=params
    )
    data = resp.json()
    items = data.get("data", {}).get("items", [])

    # Handle pagination
    page_token = data.get("data", {}).get("page_token")
    while page_token:
        params["page_token"] = page_token
        resp = requests.get(
            f"{API_URL}/{base}/tables/{table}/records",
            headers=_headers(),
            params=params
        )
        data = resp.json()
        items.extend(data.get("data", {}).get("items", []))
        page_token = data.get("data", {}).get("page_token")

    return items


def _to_ms_timestamp(date_str):
    """Convert date string to ms timestamp (Asia/Shanghai)

    Supports formats:
      - YYYY-MM-DD or YYYY/MM/DD (date only)
      - YYYY-MM-DD HH:MM (with time component)
    """
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%d %H:%M"):
        try:
            dt = datetime.strptime(date_str, fmt).replace(tzinfo=_TZ_SHANGHAI)
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

    base = get("bitable.base_app_id")
    table = get("bitable.table_id")
    resp = requests.post(
        f"{API_URL}/{base}/tables/{table}/records",
        headers=_headers(),
        json={"fields": fields}
    )
    result = resp.json()
    if result.get("code") != 0:
        raise RuntimeError(f"Feishu API error: {result}")
    return result.get("data", {}).get("record", {}).get("record_id")


async def list_uncompleted(user_id=None):
    """List uncompleted todos, optionally filtered by user"""
    items = _fetch_quick_query_records()

    result_list = []
    for item in items:
        fields = item.get("fields", {})

        # Filter by user if specified
        if user_id:
            executor_ids = _get_executor_ids(fields)
            if user_id not in executor_ids:
                continue

        result_list.append({
            "record_id": item.get("record_id"),
            "title": fields.get("待办事项", ""),
            "deadline": fields.get("截止日期"),
            "priority": fields.get("优先级"),
            "executor": fields.get("执行人"),
            "distance": fields.get("距离截止日"),
        })

    return result_list


async def get_today_stat():
    """Get today's detailed statistics for the daily report"""
    items = _fetch_view_records()
    now = datetime.now(_TZ_SHANGHAI)
    today_str = now.strftime("%Y-%m-%d")
    today_start = _to_ms_timestamp(today_str)
    today_end = today_start + 86400000 if today_start else 0

    today_new = 0
    today_due_list = []
    upcoming_list = []
    completed_list = []
    by_user = {}

    for item in items:
        fields = item.get("fields", {})
        record_id = item.get("record_id")
        title = fields.get("待办事项", "")
        priority = fields.get("优先级")
        deadline = fields.get("截止日期")
        completed = fields.get("是否已完成", False)
        created = fields.get("创建时间")

        # Get executor info
        executors = fields.get("执行人", []) or []
        user_names = ", ".join(e.get("name", "") for e in executors)

        # Count today's new items
        if created and today_start <= created < today_end:
            today_new += 1

        if completed:
            # Recently completed (created today or yesterday)
            if created and created >= today_start - 86400000:
                completed_list.append({
                    "title": title, "user": user_names, "priority": priority
                })
            continue

        # Uncompleted items - categorize by deadline (SKIP OVERDUE ITEMS)
        if deadline is None:
            continue  # no deadline, skip

        deadline_str = datetime.fromtimestamp(deadline / 1000, tz=_TZ_SHANGHAI).strftime("%Y-%m-%d")

        if today_start <= deadline < today_end:
            # Due today
            today_due_list.append({
                "title": title, "priority": priority, "user": user_names,
                "record_id": record_id
            })
        elif deadline > today_end:  # ONLY future/upcoming, SKIP OVERDUE
            # Upcoming
            days_until = int((deadline - today_end) / 86400000) + 1
            upcoming_list.append({
                "title": title, "priority": priority, "user": user_names,
                "deadline": deadline_str, "days_until": days_until,
                "record_id": record_id
            })

        # Aggregate by user - ONLY COUNT NON-OVERDUE PENDING
        for e in executors:
            name = e.get("name", "")
            if not name:
                continue
            if name not in by_user:
                by_user[name] = {"pending": 0, "high_priority": 0}
            if deadline > today_end:  # ONLY count future tasks for pending
                by_user[name]["pending"] += 1
            if priority and "P0" in priority:
                by_user[name]["high_priority"] += 1

    # Sort lists
    today_due_list.sort(key=lambda x: x.get("priority", "") or "")
    upcoming_list.sort(key=lambda x: x.get("days_until", 999))

    return {
        "date": today_str,
        "summary": {
            "today_new": today_new,
            "today_due": len(today_due_list),
            "overdue": 0,  # REMOVE OVERDUE COUNT
            "upcoming": len(upcoming_list),
            "completed_today": len(completed_list),
            "total_uncompleted": _count_uncompleted(items),
        },
        "today_due": today_due_list,
        "overdue": [],  # EMPTY OVERDUE LIST
        "upcoming": upcoming_list,
        "completed": completed_list,
        "grouped_by_user": by_user,
    }


def _count_uncompleted(items):
    cnt = 0
    for item in items:
        if not item.get("fields", {}).get("是否已完成", False):
            cnt += 1
    return cnt
