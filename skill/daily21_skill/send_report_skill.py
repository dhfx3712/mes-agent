import json
import requests

CONFIG_PATH = "/home/ubuntu/.openclaw/openclaw.json"
TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
MSG_URL = "https://open.feishu.cn/open-apis/im/v1/messages"
CHAT_ID = "oc_fee9651792b581c45e503db890cd4cf1"


def _get_credentials():
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    accounts = cfg["channels"]["feishu"]["accounts"]
    for name, acct in accounts.items():
        if acct.get("appId") == "cli_aa9d533eca3cdbe9":
            return acct["appId"], acct["appSecret"]
    raise RuntimeError("Feishu credentials not found in config")


def _get_token():
    app_id, app_secret = _get_credentials()
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

    # Send as post (rich text card)
    payload = {
        "receive_id": CHAT_ID,
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
