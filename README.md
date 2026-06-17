# mes-agent - 任务管理机器人

办公任务管理机器人，负责新增待办、查询提醒、21点自动日报。
数据存储在飞书多维表格。

## 目录结构

```
workspace-mes/
├── agents/             # Agent 配置目录
│   ├── main-agent/     # 主Agent 身份+技能
│   └── sub_agent/      # 子Agent（自建框架）
├── common/             # 共享工具函数
├── datas/              # 共享数据目录
│   ├── config.json     # 全局超参数（TODO: 从 CONFIG.md 迁移）
│   └── logs/           # 运行日志
├── flow/               # Flow 定义（自建框架）
├── intent/             # 意图定义（自建框架）
├── memory/             # 三层记忆系统
│   ├── MEMORY.md       # Layer 1: 永久知识库
│   ├── README.md       # 记忆系统使用说明
│   └── entities/       # Layer 3: 实体注册表
├── scripts/            # 业务脚本
├── skill/              # 技能定义（自建框架）
├── AGENTS.md           # Agent 架构
├── BOOTSTRAP.md        # 启动引导
├── HEARTBEAT.md        # 心跳任务
├── IDENTITY.md         # Agent 身份
├── README.md           # 本文件
├── SCRIPTS.md          # 脚本架构
├── SOUL.md             # 项目理念
├── TOOLS.md            # 指令工具清单
└── USER.md             # 用户配置
```

## 快速开始

1. 确认 `CONFIG.md` 配置正确（TODO: 迁移至 `datas/config.json`）
2. 查看 `BOOTSTRAP.md` 了解启动就绪状态
3. 通过 OpenClaw 加载项目目录
4. 使用 `/` 指令与 Agent 交互

## 配置说明

所有全局参数统一存放在 `CONFIG.md`（待迁移至 `datas/config.json`）。
