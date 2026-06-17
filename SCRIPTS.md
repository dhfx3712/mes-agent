# mes-agent - 脚本架构

## Python 虚拟环境

> 本项目所有 Python 脚本**必须**在项目专属虚拟环境中执行，禁止使用系统 Python 环境。

### 环境位置

```
scripts/.venv/          ← 虚拟环境根目录
scripts/requirements.txt ← 依赖清单
```

### 初始化流程

```bash
# 首次使用：创建虚拟环境
python3 -m venv scripts/.venv

# 安装依赖
scripts/.venv/bin/pip install -r scripts/requirements.txt
```

### Agent 调用规范

所有通过 `exec` 调用 Python 脚本时，**必须**使用虚拟环境的 Python 解释器：

```bash
# ✅ 正确：使用虚拟环境 Python
exec scripts/.venv/bin/python scripts/cli/my_script.py --arg value

# ❌ 错误：使用系统 Python
exec python3 scripts/cli/my_script.py --arg value
```

### 依赖管理

- `requirements.txt` 放在 `scripts/` 目录下，与 `.venv/` 同级
- 新增依赖时：`scripts/.venv/bin/pip install <pkg> && scripts/.venv/bin/pip freeze > scripts/requirements.txt`
- 建议锁定版本号，避免意外升级

### 注意事项

- `.venv/` 目录**不提交**到版本控制（加入 `.gitignore`）
- `requirements.txt` **必须提交**，用于环境重建
- 虚拟环境损坏时，删除 `.venv/` 后重新 `python3 -m venv` 即可
- 不同项目之间不共享虚拟环境，每个项目独立

---

## 脚本类型

| 类型 | 生命周期 | 说明 | 示例 |
|------|---------|------|------|
| **cli** | 按需调用 | 命令行客户端，每次调用启动子进程 | todo_create.py / remind_query.py / daily21_report.py |
| **one-shot** | 按需调用 | 普通业务脚本，每次调用独立运行 | skill 子脚本 |

---

## 脚本目录结构

```
scripts/
├── cli/           # CLI 客户端类
├── build/         # 数据构建类
└── utils/         # 工具函数类
```

> 当前核心脚本已迁移至 `scripts/cli/`。
> `flow/`、`agent/` 等旧目录保留作为回滚备选。

---

## 调用编排

### 编排规则

#### 新增待办

```
用户输入 → AI 提取参数(title/time/priority/content/执行人)
  → exec scripts/cli/todo_create.py '<slots>' '<ctx>'
    → common/storage.py → 飞书 Bitable
```

#### 查询提醒

```
用户输入 → AI 提取参数(days/user_id)
  → exec scripts/cli/remind_query.py '<slots>' '<ctx>'
    → common/storage.py → 飞书 Bitable
```

#### 21点日报

```
cron 触发 → exec scripts/cli/daily21_report.py --send
  → common/storage.py + send_report_skill.py → 飞书群
```

### 通用编排原则

1. **无依赖则并行**：多个独立查询/操作可同时发起
2. **有依赖则串行**：后一步依赖前一步的输出
3. **AI 介入点**：脚本无法完成的部分（如生成内容、智能判断）由 AI 处理
4. **结果合并**：并行结果全部返回后，由 AI 统一组装

### 架构说明

当前架构已从自建框架（`run_flow.py` → `flow/` → `agent/` → `skill/`）
升级为独立 CLI 脚本，直接调用 `common/storage.py` 数据层：

```
AI 层（SOUL.md 路由表）
  ↓ exec scripts/cli/<flow>.py '<slots>' '<ctx>'
脚本层（scripts/cli/）
  ↓
数据层（common/storage.py）→ 飞书 Bitable
```

旧版 `run_flow.py`、`flow/`、`agent/` 目录保留作为回滚备选。

---

## 输出格式规范

### 通用输出格式

所有脚本输出统一为 JSON 格式：

```json
{
  "status": "success | error",
  "data": { ... },
  "error": "错误信息（仅 status=error 时）"
}
```

### 业务输出格式

#### 新增待办

```json
{
  "status": "success",
  "data": {
    "record_id": "recXXX",
    "title": "待办标题",
    "priority": "🔴P0"
  }
}
```

#### 查询提醒

```json
{
  "status": "success",
  "data": [
    {
      "record_id": "recXXX",
      "title": "待办标题",
      "deadline": "2026-06-17",
      "priority": "🔴P0",
      "assignee": "沈小茜"
    }
  ]
}
```

#### 21点日报

```json
{
  "status": "success",
  "data": {
    "total": 15,
    "completed": 8,
    "pending": 7,
    "by_priority": { "P0": 3, "P1": 8, "P2": 4 },
    "by_person": { "沈小茜": 5, "于小宁": 3, "黄泡泡": 4, "白小丁": 2, "李阳": 1 }
  }
}
```

### 格式原则

1. 同一场景的输出格式**固定不变**
2. 字段顺序固定，不随意调换
3. 空数据用 `{}` 或 `[]`，不用 `null`
4. 错误信息放在 `error` 字段，不混入 `data`
