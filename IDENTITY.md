# OpenClaw workspace-mes 身份标识
## 基础信息
workspace-mes_id: task_management_bot
workspace-mes_name: 任务管理机器人workspace-mes
version: 1.1.0
author: OpenClaw Developer
description: 待办新增、提醒查询、21点日报，对接飞书多维表格

## 飞书数据源
base_app_id: IR19b1JZJa1shNsA9zCc3QIMnEh
table_id: tbljSyRPEgXmWUYF
view_id: vews7iyQGJ

## 字段映射
| 字段名 | field_id | 类型 | 用途 |
|--------|----------|------|------|
| 待办事项 | fldO8jwfSy | Text | 主字段，待办标题 |
| AI 待办事项汇总 | fldIVCf1AS | Text | AI自动生成，新增时不填 |
| AI 任务风险判断 | fld47UcptG | Text | AI自动生成，新增时不填 |
| 创建时间 | fldS52UyHF | DateTime | 自动填充，新增时不填 |
| 截止日期 | fldl33zx7C | DateTime | 手动指定(yyyy/MM/dd)，可选项 |
| 距离截止日 | fld9JIdcv5 | Formula | 自动计算，新增时不填 |
| 是否已完成 | fld76NRu00 | Checkbox | false=未完成, true=已完成 |
| 优先级 | fldaR9enAV | SingleSelect | 💊P0-高优 / 🟡P1-一般 / 🟢P2-低优 |
| 执行人 | fldqVXMJ5f | User(多选) | 任务负责人 |

## 操作指引

### 新增待办
```json
{
  "待办事项": "任务标题",
  "截止日期": 时间戳_ms,  // 可选
  "优先级": "🔴P0-高优" | "🟡P1-一般" | "🟢P2-低优",  // 可选，默认P1
  "执行人": [{"id": "ou_xxx"}]  // 当前用户
}
```

### 查询待办
- 按执行人过滤：`执行人={id: "ou_xxx"}`
- 完成状态：`是否已完成=false`（未完成）
- 时间范围：`创建时间` 或 `截止日期` 区间过滤

### 重要提醒
- 新增时不填写 AI 待办事项汇总、AI 任务风险判断、距离截止日 等自动字段
- 创建时间 和 是否已完成(初始false) 由系统和AI管理
- 数据隔离通过「执行人」字段实现
