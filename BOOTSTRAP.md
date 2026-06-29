# BOOTSTRAP.md - 启动引导

> **职责**：定义项目启动就绪检查清单和环境配置步骤。

---

## 项目概览

| 项目 | 内容 |
|------|------|
| 项目名 | mes-agent |
| 业务描述 | 办公任务管理机器人，负责新增待办、21点自动日报 |
| 架构模式 | hub-and-spoke（1 主 + 2 子：todo/daily21） |
| 数据底座 | 飞书多维表格（Bitable） |

---

## 就绪检查清单

### 配置就绪
- [x] `datas/config.json` — 全局配置已就绪
- [x] `datas/config.schema.json` — 配置校验规则已就绪
- [x] `CONFIG.md` — 配置参考文档已就绪

### 数据底座就绪
- [x] 飞书多维表格已创建（app_id: IR19b1JZJa1shNsA9zCc3QIMnEh）
- [x] 表结构已定义（待办事项/创建时间/截止日期/优先级/执行人等）
- [x] 连接信息已配置

### 记忆系统就绪
- [x] `memory/MEMORY.md` — 已创建
- [x] `memory/README.md` — 已创建
- [x] `memory/entities/` — 已创建
- [x] 会话日志自动生成

### 脚本就绪
- [x] Python 虚拟环境已创建（`scripts/.venv/`）
- [x] 依赖已安装（`scripts/requirements.txt`）
- [x] 2 个 CLI 脚本已实现（todo_create / daily21_report）
- [x] 脚本输入输出格式已标准化为 JSON

### 定时任务就绪
- [x] daily21 日报 cron 已注册（每天 21:00 Asia/Shanghai）
- [x] 任务触发动作已验证

### 架构就绪
- [x] `ARCHITECTURE.md` — 架构设计文档已创建
- [x] 数据流与实际实现一致
- [x] 配置集中化（`datas/config.json` + `common/config.py`）

### 文档治理就绪
- [x] `DOCS.md` — 文档治理规则已创建
- [x] 各文档职责边界清晰，无内容交叉

---

## 首次启动流程

```
Step 1: 确认配置  →  检查 datas/config.json
Step 2: 连接底座  →  验证飞书 Bitable 可正常读写
Step 3: 测试脚本  →  逐个运行 scripts/cli/ 下的脚本验证
Step 4: 注册 cron →  注册 daily21 定时任务
Step 5: 验收指令  →  逐条测试功能
Step 6: 正式使用  →  开始录入数据
```
