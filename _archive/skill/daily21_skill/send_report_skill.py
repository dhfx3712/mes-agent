import json
import requests

from common.config import get, get_feishu_credentials

TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
MSG_URL = "https://open.feishu.cn/open-apis/im/v1/messages"


def _get_token():
    app_id, app_secret = get_feishu_credentials("messaging")
    resp = requests.post(TOKEN_URL, json={
        "app_id": app_id,
        "app_secret": app_secret
    })
    return resp.json()["tenant_access_token"]


async def exec(content):
    """Send daily report to 工单系统 group chat"""
    token = _get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    chat_id = get("feishu.chat_id")
    # Send as post (rich text card)
    payload = {
        "receive_id": chat_id,
        "msg_type": "post",
        "content": json.dumps({
            "zh_cn": {
                "title": "📋 21点日报",
                "content": [
                    [{"tag": "text", "text": content}]
                ]
            }
        })
    }

    resp = requests.post(
        f"{MSG_URL}?receive_id_type=chat_id",
        headers=headers,
        json=payload
    )
    result = resp.json()
    if result.get("code") != 0:
        print(f"[日报推送失败] {result}")
        return False

    print(f"[日报推送成功] message_id={result.get('data', {}).get('message_id')}")
    return True
