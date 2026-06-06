import os
import requests
from datetime import datetime

BASE = "IR19b1JZJa1shNsA9zCc3QIMnEh"
TABLE = "tbljSyRPEgXmWUYF"
TOKEN = os.getenv("FEISHU_BASE_TOKEN")
URL = "https://open.feishu.cn/open-apis/bitable/v1/apps"

def today():
    return datetime.now().strftime("%Y-%m-%d")

async def save_todo(user_id, data):
    res = requests.post(f"{URL}/{BASE}/tables/{TABLE}/records",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"fields": {
            "操作用户ID": user_id,
            "待办标题": data.get("title"),
            "提醒时间": data.get("time"),
            "备注内容": data.get("content"),
            "创建日期": today()
        }})
    return res.json().get("data", {}).get("record_id")

async def get_user_remind(user_id, days=1):
    f = f'AND({{操作用户ID}}="{user_id}",{{创建日期}}>=DATEADD(TODAY(),-{days},"day"))'
    res = requests.get(f"{URL}/{BASE}/tables/{TABLE}/records?filter={f}",
        headers={"Authorization": f"Bearer {TOKEN}"})
    return [{"title": i["fields"].get("待办标题"),
             "remind_time": i["fields"].get("提醒时间")}
            for i in res.json().get("data", {}).get("items", [])]

async def get_today_stat():
    f = f'{{创建日期}}="{today()}"'
    res = requests.get(f"{URL}/{BASE}/tables/{TABLE}/records?filter={f}",
        headers={"Authorization": f"Bearer {TOKEN}"})
    cnt = len(res.json().get("data", {}).get("items", []))
    return {"todo_cnt": cnt, "remind_cnt": cnt}
