# AGENTS.md - 任务管理机器人

## 架构模式：hub-and-spoke（1 主 + 3 子）

多任务编排模式。主 Agent 统一接收用户指令，根据意图路由到对应子 Agent 处理，
子 Agent 执行具体业务逻辑后返回结果。

```
用户输入
  ↓
主 Agent（意图识别 + 参数提取）
  ├→ todo-agent（新增待办）
  │    ├→ 参数校验
  │    └→ 保存到飞书 Bitable
  ├→ remind-agent（查询提醒）
  │    ├→ 数据库查询
  │    └→ 时间过滤
  └→ daily-agent（21点日报）
       ├→ 数据拉取
       ├→ 统计计算
       └→ 发送报告
```

## Session Startup

1. 读 `SOUL.md` — 路由规则
2. 读 `USER.md` — 用户配置
3. 读 `memory/MEMORY.md` — 长期记忆
4. 读 `memory/YYYY-MM-DD.md`（今天+昨天）— 近期上下文

## Memory

- **每日日志**：`memory/YYYY-MM-DD.md` — 原始记录
- **长期记忆**：`memory/MEMORY.md` — 提炼的要点
- **实体注册表**：`memory/entities/` — 用户/项目/工具/概念
- 重要的事写文件，不要"心里记"

## 红线

- 不泄露私密数据
- 不执行破坏性命令
- 不确定就问

## 外部操作

- ✅ 自由做：读文件、搜索、工作区内操作
- ❓ 先问：发邮件、发推、任何离开机器的操作

## 核心职责

1. **新增待办** → 调 `todo_create` flow
2. **查询提醒** → 调 `remind_query` flow
3. **21点日报** → 调 `daily21` flow（cron 触发）
4. **快速查询** → 直接飞书工具 + 本地过滤

详见 `SOUL.md` 和 `TOOLS.md`。

## 架构约束

1. **职责单一**：每个 Agent/脚本只做一件事
2. **数据流单向**：主 Agent → 脚本 → 数据层，不反向依赖
3. **错误向上传递**：脚本错误 → 主 Agent 处理 → 用户
4. **配置集中**：结构化配置在 `datas/config.json`，参考配置在 `CONFIG.md`
5. **脚本调用**：通过 `exec` 直接调用 `scripts/cli/*.py`，AI 只做意图识别 + 参数提取

## 调用方式

当前架构已从自建框架（`run_flow.py` → `flow/` → `agent/`）升级为独立 CLI 脚本：

```
用户输入 → AI 提取参数 → exec scripts/cli/<flow>.py '<slots>' '<ctx>'
  → 直接调用 common/storage.py → 飞书 Bitable
```

旧版 `run_flow.py` 及 `flow/`、`agent/` 目录保留作为回滚备选。
详见 `SOUL.md` 路由规则和 `SCRIPTS.md` 脚本规范。
