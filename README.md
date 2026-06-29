# mes-agent - 任务管理机器人

办公任务管理机器人，负责新增待办、21点自动日报。
数据存储在飞书多维表格。

## 目录结构

```
workspace-mes/
├── agents/             # Agent 配置目录
├── scripts/            # 业务脚本
│   └── cli/            # 独立 CLI 脚本（核心业务）
├── common/             # 公共模块（storage/config）
├── datas/              # 结构化配置
│   ├── config.json     # 全局配置
│   └── config.schema.json  # 配置校验规则
├── memory/             # 三层记忆系统
│   ├── MEMORY.md       # Layer 1: 永久知识库
│   ├── README.md       # 记忆系统使用说明
│   └── entities/       # Layer 3: 实体注册表
├── _archive/           # 旧自建框架（回滚备选）
├── AGENTS.md           # 最高优先级执行流程
├── ARCHITECTURE.md     # 系统架构
├── BOOTSTRAP.md        # 启动引导
├── CONFIG.md           # 配置参考
├── DOCS.md             # 文档治理规则
├── HEARTBEAT.md        # 心跳任务
├── IDENTITY.md         # 产品能力边界
├── README.md           # 本文件
├── SCRIPTS.md          # 脚本架构
├── SOUL.md             # 人格、语气、输出风格
├── TOOLS.md            # 工具调用方式
└── USER.md             # 用户画像
```

## 快速开始

1. 确认 `datas/config.json` 配置正确
2. 查看 `BOOTSTRAP.md` 了解启动就绪状态
3. 通过 OpenClaw 加载项目目录
4. 使用 `/` 指令与 Agent 交互

## 配置说明

所有全局参数统一存放在 `datas/config.json`，`CONFIG.md` 作为参考文档。
