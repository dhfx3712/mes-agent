# mes-agent — 系统架构

> **职责**：统一解释本项目的系统架构，包括架构模式、数据流、集成契约、定时任务。所有与架构相关的内容集中于此，其他文档通过引用指向本文件。

---

## 1. 架构模式

**模式：hub-and-spoke（1 主 + 3 子）**

多任务编排模式。主 Agent 统一接收用户指令，根据意图路由到对应业务脚本处理，脚本执行具体业务逻辑后返回结果。

```
用户输入
  ↓
主 Agent（意图识别 + 参数提取）
  ├→ todo_create.py（新增待办）
  │    └→ common/storage.py → 飞书 Bitable
  └→ daily21_report.py（21点日报）
       └→ common/storage.py → 飞书群
```

---

## 2. 数据流

```
AI 层（AGENTS.md 路由表）
  │  职责：意图识别 + 参数提取
  │  输出：exec scripts/cli/<flow>.py '<slots_json>' '<ctx_json>'
  ▼
脚本层（scripts/cli/）
  │  职责：执行业务逻辑、数据校验
  │  输出：stdout JSON
  ▼
数据层（common/storage.py）
  │  职责：飞书 API 封装、CRUD 操作
  ▼
数据底座（飞书多维表格 Bitable）
```

### 数据流说明

| 环节 | 输入 | 处理 | 输出 | 错误处理 |
|------|------|------|------|---------|
| 意图识别 | 用户自然语言 | AI 提取 slots + ctx | slots_json + ctx_json | 参数缺失时提示用户补充 |
| 脚本执行 | slots_json + ctx_json | CLI 脚本执行业务逻辑 | stdout JSON | 脚本返回 `{"status":"error"}`，AI 向用户展示错误 |
| 数据持久化 | 结构化字段 | common/storage.py 调用飞书 API | 飞书 Bitable 记录 | API 异常时返回错误信息 |

---

## 3. 架构约束

1. **职责单一**：每个脚本只做一件事
2. **数据流单向**：主 Agent → 脚本 → 数据层，不反向依赖
3. **错误向上传递**：脚本错误 → 主 Agent 处理 → 用户
4. **配置集中**：结构化配置在 `datas/config.json`，通过 `common/config.py` 读取
5. **AI 边界**：AI 只做意图识别 + 参数提取，确定性逻辑交给 Python 脚本

---

## 4. 脚本集成契约

### 调用规范

| 维度 | 规范 |
|------|------|
| 调用方式 | `exec` 命令调用 |
| 输入方式 | 命令行参数 JSON（slots + ctx） |
| 输出格式 | stdout 输出 JSON（`{"status":"success","data":...}`） |
| 成功标志 | `status: "success"` |
| 错误标志 | `status: "error"`，`error` 字段描述问题 |
| 超时处理 | 默认 30s 超时，超时视为失败 |

### 脚本清单

| 脚本 | 用途 | 调用方 | 输入参数 | 输出格式 |
|------|------|--------|---------|---------|
| `scripts/cli/todo_create.py` | 新增待办 | 主 Agent | slots: title(必填), time, content, priority; ctx: user_id | `{"record_id": "recXXX"}` |
| `scripts/cli/daily21_report.py` | 21点日报 | cron 触发 | `--send` 推送到飞书群 | `{"content": "markdown..."}` |

> 详细输出格式见 `SCRIPTS.md`「输出格式规范」章节。

---

## 5. 定时任务

### 任务清单

| 任务名 | 调度表达式 | 触发动作 | 执行脚本 | 结果处理 |
|--------|-----------|---------|---------|---------|
| daily21 日报 | `0 21 * * *` (Asia/Shanghai) | 生成日报并推送飞书群 | `scripts/cli/daily21_report.py --send` | 推送成功/失败日志记录 |

### 注册方式

通过 OpenClaw cron 模块注册，配置见 `cron/daily21_cron.json`：

```json
{
  "task": "daily21_report",
  "cron": "0 21 * * *",
  "tz": "Asia/Shanghai"
}
```

---

## 6. 错误处理模式

| 错误类型 | 处理策略 | 重试策略 | 通知方式 |
|---------|---------|---------|---------|
| 参数缺失 | 提示用户补充 | 不重试 | 直接回复用户 |
| 脚本执行失败 | 展示错误信息 | 不重试 | 直接回复用户 |
| 飞书 API 异常 | 捕获异常返回错误 | 不重试 | 直接回复用户 |
| cron 任务失败 | 记录日志 | 下次调度自动重试 | 日志记录 |

---

## 7. 历史架构演进

### 当前架构（v2 — 独立 CLI 脚本）

```
AI 层（AGENTS.md 路由表）
  ↓ exec scripts/cli/<flow>.py '<slots>' '<ctx>'
脚本层（scripts/cli/）
  ↓
数据层（common/storage.py）→ 飞书 Bitable
```

### 旧架构（v1 — 自建框架，已归档）

```
AI 层 → run_flow.py → flow/ → skill/ → common/ → 飞书 Bitable
```

旧版 `run_flow.py`、`flow/`、`agent/`、`skill/`、`intent/` 目录已归档至 `_archive/`，保留作为回滚备选。
