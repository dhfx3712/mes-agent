# BOOTSTRAP.md - 启动引导

## 项目概览

| 项目 | 内容 |
|------|------|
| 项目名 | mes-agent |
| 业务描述 | 办公任务管理机器人，负责新增待办、查询提醒、21点自动日报 |
| 架构模式 | hub-and-spoke（1 主 + 3 子：todo/remind/daily21） |
| 数据底座 | 飞书多维表格（Bitable） |

---

## 就绪检查清单

### 配置就绪
- [x] `CONFIG.md` — 飞书 Bitable 配置已填写
- [ ] `datas/config.json` — TODO: 从 CONFIG.md 迁移
- [ ] `datas/config.schema.json` — TODO: 新增配置校验规则

### 数据底座就绪
- [x] 飞书多维表格已创建（app_id: IR19b1JZJa1shNsA9zCc3QIMnEh）
- [x] 表结构已定义（待办事项/创建时间/截止日期/优先级/执行人等）
- [x] 连接信息已配置

### 记忆系统就绪
- [x] `memory/MEMORY.md` — 已创建
- [x] `memory/README.md` — 已创建
- [x] `memory/entities/` — 已创建
- [ ] 首次会话后自动生成 `memory/YYYY-MM-DD.md` 会话日志

### 脚本就绪
- [x] Python 虚拟环境已创建（`scripts/.venv/`）
- [ ] 依赖已安装（`scripts/requirements.txt`）
- [x] 业务脚本已编写（`common/` + `skill/` + `flow/`）
- [ ] 脚本输入输出格式符合集成契约

### 定时任务就绪
- [x] daily21 日报 cron 已注册（`cron/daily21_cron.json`）
- [x] 任务触发动作已验证
- [ ] 失败处理策略已确认

### 架构就绪
- [ ] `ARCHITECTURE.md` — TODO: 新增架构设计文档
- [ ] 状态机定义与实际逻辑一致
- [ ] 数据流与实际实现一致

### 复杂业务就绪（flow/skill 分层架构）
- [x] 自建 flow/skill 分层架构已运行
- [x] `run_flow.py` 桥接脚本已创建
- [x] `flow/` 目录已创建，每个业务一个 flow 目录
- [x] `skill/` 目录已创建，原子技能已拆分
- [x] `common/` 目录已创建，共享工具函数已提取
- [x] SOUL.md 路由表已配置（AI 只做意图识别 + 参数提取）
- [x] 每个 skill 可独立运行测试通过

---

## 首次启动流程

```
Step 1: 确认配置  →  检查 CONFIG.md 飞书配置
Step 2: 连接底座  →  验证飞书 Bitable 可正常读写
Step 3: 测试脚本  →  逐个运行 flow/ 下的 flow 验证
Step 4: 注册 cron →  注册 daily21 定时任务
Step 5: 验收指令  →  逐条测试 TOOLS.md 中的指令
Step 6: 正式使用  →  开始录入数据
```

---

## 已知待办

- [ ] CONFIG.md → `datas/config.json` + `datas/config.schema.json` 迁移
- [ ] 新增 `ARCHITECTURE.md` 架构设计文档
- [ ] 自建框架（intent/flow/skill/agent）→ OpenClaw 原生机制迁移
- [ ] 脚本输入输出格式标准化为 JSON
