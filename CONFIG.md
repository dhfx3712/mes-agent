# 任务管理机器人配置

## 数据源
- **base_app_id**: IR19b1JZJa1shNsA9zCc3QIMnEh
- **table_id**: tbljSyRPEgXmWUYF
- **view_id**: vews7iyQGJ

## 字段映射
| 字段名 | field_id | 类型 | 说明 |
|--------|----------|------|------|
| 待办事项 | fldO8jwfSy | Text | 主字段 |
| AI 待办事项汇总 | fldIVCf1AS | Text | 自动生成，新增不填 |
| AI 任务风险判断 | fld47UcptG | Text | 自动生成，新增不填 |
| 创建时间 | fldS52UyHF | DateTime | 自动填充 |
| 截止日期 | fldl33zx7C | DateTime | yyyy/MM/dd |
| 距离截止日 | fld9JIdcv5 | Formula | 自动计算 |
| 是否已完成 | fld76NRu00 | Checkbox | false=未完成 |
| 优先级 | fldaR9enAV | SingleSelect | 🔴P0 / 🟡P1 / 🟢P2 |
| 执行人 | fldqVXMJ5f | User(多选) | 任务负责人 |

## 执行人映射（open_id）
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

## 脚本调用规范
```bash
python3 scripts/cli/<script>.py '<slots_json>' '<ctx_json>'
```

| 脚本 | 功能 | slots | ctx |
|------|------|-------|-----|
| todo_create.py | 新增待办 | title(必填), time, content, priority | user_id |
| remind_query.py | 查询提醒 | days(默认1) | user_id |
| daily21_report.py | 21点日报 | 无 | 无 |

> 旧版 `run_flow.py` 已废弃，保留作为回滚备选。

## 路由规则
1. **新增待办** → `scripts/cli/todo_create.py`：提取 title/time/priority/content，确定执行人（"我"=当前用户，他人查映射表）
2. **查询提醒** → `scripts/cli/remind_query.py`：提取 days(默认1)/user_id
3. **21点日报** → `scripts/cli/daily21_report.py --send`：cron 自动触发
4. **快速查询**（不走脚本）→ `feishu_bitable_list_records` + 本地过滤

## 待办标题最大长度
100

## 默认查询范围
最近 1 天
