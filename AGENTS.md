# AGENTS.md — 最高优先级执行流程

> **职责**：定义本项目的最高优先级执行流程。当本文件与其他文档冲突时，以本文件为准。
>
> 架构模式详情见 `ARCHITECTURE.md`。
> 工具清单详情见 `TOOLS.md`。
> 人格风格详情见 `SOUL.md`。

---

## 1. 文档优先级

当多个项目文档内容不一致时，按以下顺序执行：

1. **AGENTS.md**：最高优先级执行流程
2. **TOOLS.md**：工具调用规范
3. **SOUL.md**：人格、语气、输出风格
4. **IDENTITY.md**：能力边界
5. **USER.md**：用户画像
6. **ARCHITECTURE.md**：架构说明
7. **README.md / CONFIG.md / 历史记忆**：参考信息

历史会话和记忆只能辅助理解背景，不能覆盖当前文件定义的标准流程。

---

## 2. Session Startup

每次会话启动时，按以下顺序加载上下文：

1. 读 `SOUL.md` — 人格、语气、输出风格
2. 读 `USER.md` — 用户配置
3. 读 `memory/MEMORY.md` — 长期记忆
4. 读 `memory/YYYY-MM-DD.md`（今天+昨天）— 近期上下文

---

## 3. 核心职责

| # | 职责 | 处理方式 |
|---|------|---------|
| 1 | **新增待办** | 提取参数 → 调 `scripts/cli/todo_create.py` |
| 2 | **21点日报** | cron 自动触发 → `scripts/cli/daily21_report.py --send` |
| 3 | **快速查询** | 直接 `feishu_bitable_list_records` + 本地过滤 |

---

## 4. 路由规则

### 4.1 新增待办

```bash
exec scripts/.venv/bin/python scripts/cli/todo_create.py '<slots_json>' '<ctx_json>'
```

| 参数 | 必填 | 说明 |
|------|------|------|
| slots.title | ✅ | 待办标题（最大100字） |
| slots.time | ❌ | 截止日期，格式 YYYY-MM-DD；若包含具体时间（如 `2026-06-24 18:00`），同时创建 cron 到点提醒 |
| slots.content | ❌ | 待办详情 |
| slots.priority | ❌ | 🔴P0 / 🟡P1（默认） / 🟢P2 |
| ctx.user_id | ✅ | 执行人 open_id |

**执行人确定规则：**
- "我" → 当前用户的 open_id
- 他人姓名 → 查 `datas/config.json` 中 `executor_mapping` 映射表

**带时间点的待办（额外创建 cron 提醒）：**

如果 `slots.time` 包含具体时间（如 `2026-06-24 18:00`），在写飞书表格后，额外创建一次性 cron 提醒：

```json
{
  "name": "remind-{title}",
  "schedule": { "kind": "at", "at": "{ISO时间}" },
  "payload": {
    "kind": "systemEvent",
    "text": "⏰ 待办提醒：{title}"
  },
  "sessionTarget": "current",
  "deleteAfterRun": true
}
```

**时间判断规则：**
- `2026-06-30` → 仅截止日期，只写表格
- `2026-06-24 18:00` → 含具体时间，写表格 + 创建 cron

### 4.2 21点日报

```bash
exec scripts/.venv/bin/python scripts/cli/daily21_report.py --send
```

- cron 自动触发（每天 21:00 Asia/Shanghai）
- `--send` 推送到飞书群

### 4.3 快速查询（不走脚本）

直接使用 `feishu_bitable_list_records` 工具拉取数据，本地过滤。

---

## 5. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| 参数缺失（如无标题） | 提示用户补充，终止 |
| 执行人未知 | 提示用户确认执行人 |
| 脚本返回 error | 展示错误信息给用户 |
| 飞书 API 异常 | 提示"数据服务异常，请稍后重试" |

---

## 6. 安全边界

- 不泄露私密数据
- 不执行破坏性命令
- 不确定就问
- 不替用户发送外部消息，除非用户明确要求且操作安全

## 7. 外部操作

- ✅ 自由做：读文件、搜索、工作区内操作
- ❓ 先问：发邮件、发推、任何离开机器的操作

## 8. Heartbeat 规则

如果收到 heartbeat 轮询：
1. 读取 `HEARTBEAT.md`
2. 只执行 HEARTBEAT.md 中明确写出的任务
3. 不从旧会话或历史记忆中推断额外任务
4. 如果没有需要处理的任务，只回复：`HEARTBEAT_OK`
