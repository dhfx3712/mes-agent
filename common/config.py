"""Configuration loader — reads datas/config.json and provides typed access.

All business configuration (Bitable IDs, field mappings, executor mappings, etc.)
is centralized in datas/config.json. Credentials (appSecret) remain in openclaw.json.
"""
import json
import os
from typing import Any

_CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CONFIG_PATH = os.path.join(_CONFIG_DIR, "datas", "config.json")
_OPENCLAW_CONFIG_PATH = os.path.join(_CONFIG_DIR, "..", "openclaw.json")

_cache: dict[str, Any] | None = None


def _load() -> dict[str, Any]:
    global _cache
    if _cache is None:
        with open(_CONFIG_PATH) as f:
            _cache = json.load(f)
    return _cache


def reload():
    """Force reload config from disk (useful after config changes)."""
    global _cache
    _cache = None
    _load()


def get(key: str, default: Any = None) -> Any:
    """Get a config value by dot-separated key path.

    Example: get("bitable.base_app_id") -> "IR19b1JZJa1shNsA9zCc3QIMnEh"
    """
    data = _load()
    parts = key.split(".")
    for part in parts:
        if isinstance(data, dict):
            data = data.get(part)
            if data is None:
                return default
        else:
            return default
    return data


def get_feishu_credentials(app_key: str) -> tuple[str, str]:
    """Get (app_id, app_secret) from openclaw.json for a given app key.

    Args:
        app_key: Key in datas/config.json feishu.apps, e.g. "bitable" or "messaging"
    """
    app_id = get(f"feishu.apps.{app_key}.appId")
    if not app_id:
        raise RuntimeError(f"Feishu app key '{app_key}' not found in datas/config.json")

    with open(_OPENCLAW_CONFIG_PATH) as f:
        cfg = json.load(f)
    accounts = cfg.get("channels", {}).get("feishu", {}).get("accounts", {})
    for name, acct in accounts.items():
        if acct.get("appId") == app_id:
            return acct["appId"], acct["appSecret"]
    raise RuntimeError(f"Feishu credentials for appId '{app_id}' not found in openclaw.json")
