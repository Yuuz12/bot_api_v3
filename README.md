# BotApiV3

基于 FastAPI 的多功能机器人后端 API，为 QQ 机器人、Web 应用等提供用户管理、内容审核、AI 对话、游戏数据查询、RSS 订阅、抽奖系统等一系列服务。

## ✨ 功能模块

- **用户系统** – 注册、登录、签到、签到图
- **回声洞** – 匿名留言/树洞功能
- **Minecraft** – 服务器状态查询、玩家信息
- **RSS / B站订阅** – RSS 源管理、B站动态订阅与推送
- **抽奖系统** – 奖池管理、抽奖逻辑
- **邀请码** – 邀请码生成与校验
- **MOAuth** – 第三方 OAuth 接入
- **统计** – 各类使用数据统计
- **AI助手** – 对接 DeepSeek / Qwen 等大模型对话
- **番剧数据** – 番剧信息查询
- **BT面板** – BT 面板相关操作
- **百度审核** – 百度内容审核 API 接入
- **邮件服务** – 邮件发送
- **Myuz** – 自定义功能
- **osu!** – osu! 玩家卡片生成
- **Storm** – 图片生成

## 🛠 技术栈

- **Web 框架**: FastAPI
- **ORM**: SQLAlchemy + Alembic
- **数据验证**: Pydantic v2
- **数据库**: PostgreSQL / MySQL（通过 SQLAlchemy 支持）
- **包管理**: uv
- **服务器**: Uvicorn
- **其它**: httpx、Pillow 等

## 📁 项目结构

botapiv3/
├── .env.example # 环境变量模板
├── .gitignore
├── pyproject.toml # 项目配置与依赖
├── alembic.ini # 数据库迁移配置
├── alembic/ # 数据库迁移脚本
├── app/
│ ├── main.py # FastAPI 应用入口
│ ├── config.py # 配置管理（pydantic-settings）
│ ├── database.py # 数据库连接与会话管理
│ ├── dependencies.py # 通用依赖（鉴权、分页等）
│ ├── exceptions.py # 自定义异常与错误处理
│ ├── models/ # SQLAlchemy ORM 模型
│ ├── schemas/ # Pydantic 请求/响应模型
│ ├── routers/ # API 路由（按模块拆分）
│ ├── services/ # 业务逻辑层
│ └── utils/ # 工具函数
├── static/ # 静态资源
└── tests/ # 测试


## 🚀 快速开始

### 前提条件

- Python 3.11+
- 一个受支持的数据库（如 PostgreSQL、MySQL），并已创建对应的数据库

### 1. 克隆仓库

```bash
git clone https://github.com/Yuuz12/bot_api_v3
```

### 2. 配置环境变量

```bash
cp .env.example .env
```
编辑 .env 文件，填入数据库连接信息、各类 API Key 等必需配置。

### 3. 安装依赖

```bash
uv sync                # 安装生产依赖
uv sync --group dev    # 安装开发依赖（可选）
```

### 4. 数据库迁移（可选）

```bash
uv run alembic upgrade head
```

### 5. 启动服务

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📖 API 文档
启动服务后，FastAPI 自动生成交互式文档：

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc
