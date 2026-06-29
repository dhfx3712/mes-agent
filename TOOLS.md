# TOOLS.md — 工具调用方式

> **职责**：定义本项目的所有指令及其调用方式。
>
> 执行流程详情见 `AGENTS.md`。
> 架构模式详情见 `ARCHITECTURE.md`。

---

## 1. 用户指令

### 业务指令

| 指令 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `新增待办` / `添加任务` | 创建一条待办事项，含具体时间点时同时创建 cron 到点提醒 | 标题、截止日期/时间、优先级、执行人 | 创建结果摘要 |
| `快速查询` / `看看有什么` / `我的待办` | 直接查询飞书表格 | 无 | 待办列表 |

### 系统指令

| 指令 | 功能 |
|------|------|
| `/架构` | 查看架构设计文档（ARCHITECTURE.md） |
| `/配置` | 查看当前配置参考（CONFIG.md） |

## 2. 脚本调用规范

所有通过 `exec` 调用 Python 脚本时，**必须**使用虚拟环境的 Python 解释器：

```bash
# ✅ 正确
exec scripts/.venv/bin/python scripts/cli/<script>.py '<slots_json>' '<ctx_json>'

# ❌ 错误（禁止使用系统 Python）
exec python3 scripts/cli/<script>.py ...
```

> 详细脚本规范见 `SCRIPTS.md`。
> 虚拟环境配置见 `SCRIPTS.md`「Python 虚拟环境」章节。
