# TOOLS.md - Local Notes

# 全局工具
1. storage_ops：飞书Base读写
2. time_parse：时间解析
数据源：IR19b1JZJa1shNsA9zCc3QIMnEh / tbljSyRPEgXmWUYF

# Flow 调用规范 (SOP)
调用路径：`python3 run_flow.py <flow_name> '<slots_json>' '<ctx_json>'`

## flow_name 列表
| flow_name | 功能 | slots | ctx 参数 |
|---|---|---|---|
| todo_create | 新增待办 | title(必填), time(可选), content(可选), priority(可选) | user_id |
| remind_query | 查询提醒 | days(可选,默认1) | user_id |
| daily21 | 21点日报 | 无 | 无 |

## 新增待办模板 (todo_create)
```
python3 run_flow.py todo_create '{"title":"...", "time":"2026-06-07", "priority":"🔴P0-高优"}' '{"user_id":"ou_xxx"}'
```

## 飞书执行人映射（open_id）
| 姓名 | open_id |
|------|---------|
| 沈小茜 | ou_a6b449d468fbe921b03e6a1c62e0e946 |
| 于小宁 | ou_8e3f6e32ecb9aea3f0321e2e026835b0 |
| 黄泡泡 | ou_71c967f85c3e8022c4331fa3ffac1826 |
| 白小丁 | ou_c1411be3fd804acdeba1d36639c3dba0 |
| 李阳 | ou_8ba41bd5afdf8b5bba14eaf1e89800c5 |
| 用户765969 | ou_4c9b0020833a979373d21a892f2d33ea |

## 优先级选项
- 🔴P0-高优（紧急重要）
- 🟡P1-一般（默认）
- 🟢P2-低优（不急）
