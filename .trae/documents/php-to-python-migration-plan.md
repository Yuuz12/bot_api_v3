# botapiv2 PHP → Python 迁移与代码优化计划

## 项目现状分析

当前项目是一个名为 **MIKUCHAT** 的聊天机器人后端 API 系统，基于 PHP 构建，包含约 50+ 个 PHP 文件，每个文件对应一个独立的 API 端点。

### 核心问题

| 类别 | 问题描述 | 严重程度 |
|------|---------|---------|
| **SQL 注入** | 所有数据库操作均使用字符串拼接，`PDO::prepare()` 形同虚设 | 🔴 致命 |
| **凭据泄露** | 数据库密码、SMTP 授权码、API Key 全部硬编码在源码中 | 🔴 致命 |
| **鉴权不统一** | 部分使用 `auth_key()`，部分硬编码 key，部分无鉴权 | 🔴 严重 |
| **代码大量重复** | user 模块每个 update 文件结构几乎相同，email 两个文件 100% 重复 | 🟡 中等 |
| **无输入验证** | 绝大多数接口未对输入进行类型、长度、格式验证 | 🔴 严重 |
| **无错误处理** | 数据库操作无 try-catch，PDO 异常未捕获 | 🟡 中等 |
| **无事务保护** | 多表操作无事务，存在数据不一致风险 | 🟡 中等 |
| **数据库连接无复用** | 每次操作新建 PDO 连接，性能极差 | 🟡 中等 |
| **SSL 验证禁用** | cURL 请求禁用 SSL 证书验证 | 🟡 中等 |
| **CORS 全开** | `Access-Control-Allow-Origin:*` 允许任何域跨域访问 | 🟡 中等 |

---

## 技术选型

| 组件 | 选型 | 理由 |
|------|------|------|
| **Web 框架** | FastAPI | 异步高性能、自动 OpenAPI 文档、类型安全、Pydantic 验证 |
| **ORM** | SQLAlchemy 2.0 + Alembic | 成熟稳定、支持异步、参数化查询杜绝 SQL 注入 |
| **数据验证** | Pydantic v2 | 与 FastAPI 深度集成，自动请求验证和序列化 |
| **HTTP 客户端** | httpx | 支持异步、API 风格与 requests 一致 |
| **图片处理** | Pillow | 替代 PHP ImageMagick，Python 生态最成熟的图片库 |
| **邮件发送** | aiosmtplib | 异步 SMTP 客户端 |
| **配置管理** | pydantic-settings | 环境变量 + .env 文件，杜绝硬编码凭据 |
| **MC Ping** | mcstatus | Python 成熟库，替代自写 MinecraftPing |
| **RSS 解析** | feedparser | Python 标准 RSS 解析库 |

---

## 新项目结构

```
botapiv2/
├── .env.example                    # 环境变量模板
├── .gitignore
├── pyproject.toml                  # 项目配置与依赖
├── alembic.ini                     # 数据库迁移配置
├── alembic/                        # 数据库迁移脚本
│   ├── env.py
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI 应用入口
│   ├── config.py                   # 配置管理（pydantic-settings）
│   ├── database.py                 # 数据库连接与会话管理
│   ├── dependencies.py             # 通用依赖（鉴权、分页等）
│   ├── exceptions.py               # 自定义异常与错误处理
│   ├── models/                     # SQLAlchemy ORM 模型
│   │   ├── __init__.py
│   │   ├── user.py                 # 用户表
│   │   ├── cave.py                 # 回声洞表
│   │   ├── minecraft.py            # MC 相关表
│   │   ├── rss.py                  # RSS/B站订阅表
│   │   ├── prize.py                # 奖池/抽奖表
│   │   ├── invitation.py           # 邀请码表
│   │   ├── moauth.py               # MOAuth 表
│   │   ├── statistics.py           # 统计表
│   │   └── baidu.py                # 百度 API token 表
│   ├── schemas/                    # Pydantic 请求/响应模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── cave.py
│   │   ├── minecraft.py
│   │   ├── rss.py
│   │   ├── prize.py
│   │   ├── invitation.py
│   │   ├── moauth.py
│   │   ├── statistics.py
│   │   └── common.py               # 通用响应模型
│   ├── routers/                    # API 路由（按模块拆分）
│   │   ├── __init__.py
│   │   ├── user.py                 # /api/user/*
│   │   ├── cave.py                 # /api/cave/*
│   │   ├── minecraft.py            # /api/minecraft/*
│   │   ├── rss.py                  # /api/rss/*
│   │   ├── prize.py                # /api/prize/*
│   │   ├── invitation.py           # /api/invitation/*
│   │   ├── moauth.py               # /api/moauth/*
│   │   ├── statistics.py           # /api/statistics/*
│   │   ├── assistant.py            # /api/assistant/*
│   │   ├── bangumi.py              # /api/bangumi/*
│   │   ├── btsoft.py               # /api/btsoft/*
│   │   ├── baidu.py                # /api/baidu/*
│   │   ├── doujinshi.py            # /api/doujinshi/*
│   │   ├── email.py                # /api/email/*
│   │   ├── myuz.py                 # /api/myuz/*
│   │   ├── osu.py                  # /api/osu/*
│   │   └── storm.py                # /api/storm/*
│   ├── services/                   # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── cave_service.py
│   │   ├── prize_service.py
│   │   ├── assistant_service.py    # AI 对话（DeepSeek/Qwen）
│   │   ├── email_service.py        # 邮件发送
│   │   ├── btsoft_service.py       # 宝塔面板
│   │   ├── baidu_service.py        # 百度审核
│   │   ├── minecraft_service.py    # MC 服务器查询
│   │   ├── osu_service.py          # osu! 卡片生成
│   │   ├── storm_service.py        # 图片生成
│   │   └── rss_service.py          # RSS 管理
│   └── utils/                      # 工具函数
│       ├── __init__.py
│       ├── http.py                 # HTTP 客户端封装
│       ├── image.py                # 图片处理工具
│       └── security.py             # 安全工具（token 生成等）
├── static/                         # 静态资源
│   ├── flags/                      # 国旗图片（合并去重）
│   ├── fonts/                      # 字体文件（合并去重）
│   ├── img/                        # 其他图片资源
│   └── templates/                  # 模板图片（storm 模块）
└── tests/                          # 测试
    ├── __init__.py
    ├── conftest.py
    ├── test_user.py
    ├── test_cave.py
    └── ...
```

---

## 实施步骤

### 阶段一：项目基础设施搭建

#### 1.1 初始化 Python 项目
- 创建 `pyproject.toml`，声明所有依赖
- 配置 `.gitignore`（排除 `.env`、`__pycache__`、`.venv` 等）
- 创建 `.env.example`，列出所有需要的环境变量
- 创建 Python 虚拟环境

#### 1.2 配置管理
- 创建 `app/config.py`，使用 `pydantic-settings` 从环境变量读取所有敏感信息：
  - 数据库连接信息（host、port、dbname、user、password）
  - API Keys（DeepSeek、Qwen、osu!、百度、宝塔面板）
  - SMTP 凭据（邮箱、授权码）
  - 鉴权 token
- 所有凭据不再硬编码，统一通过环境变量注入

#### 1.3 数据库层
- 创建 `app/database.py`：
  - 使用 SQLAlchemy 2.0 异步引擎
  - 连接池配置（替代每次新建连接）
  - 会话管理（依赖注入方式）
- 创建所有 ORM 模型（`app/models/`）：
  - `User` 模型：对应 `user` 表
  - `Cave` / `CaveRecycle` 模型：对应 `cave` / `cave_recycle` 表
  - `MCBlacklist` / `MCBlacklistRecycle` 模型
  - `MCServer` 模型
  - `BilibiliSub` 模型（从 minecraft/server 目录迁移，修正命名）
  - `RSSSub` 模型
  - `Prize` / `PrizeUser` 模型
  - `InvitationCode` / `InvitationQQ` / `InvitationNumber` 模型
  - `MOAuth` 模型
  - `Statistics` 模型
  - `BaiduApplication` 模型
  - `AuthKey` 模型
  - `Item` 模型
- 配置 Alembic 数据库迁移

#### 1.4 通用基础设施
- 创建 `app/exceptions.py`：统一异常类和全局异常处理器
- 创建 `app/dependencies.py`：
  - `get_db()`：数据库会话依赖
  - `verify_token()`：统一鉴权依赖（替代散落各处的 auth_key）
  - `get_current_user()`：获取当前用户
- 创建 `app/utils/http.py`：httpx 异步客户端封装（启用 SSL 验证）
- 创建 `app/utils/security.py`：安全工具（随机码生成用 `secrets` 模块）

#### 1.5 FastAPI 应用入口
- 创建 `app/main.py`：
  - CORS 中间件（配置允许的域名，不再 `*` 全开）
  - 全局异常处理
  - 路由注册
  - 生命周期管理（启动/关闭时初始化/清理资源）

---

### 阶段二：核心模块迁移

#### 2.1 用户模块 (`app/routers/user.py` + `app/services/user_service.py`)

**合并优化**：原 PHP 中 user 目录下有 20+ 个文件，每个文件只做一件小事。Python 版合并为一个路由文件，按功能分组：

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/user/` | POST | insert_user.php | Pydantic 验证 QQ 号格式 |
| `/api/user/info` | GET | get_user_info.php | 合并三个查询分支为统一接口 |
| `/api/user/check` | POST | update_user_check.php | 修正返回数据不一致问题，合并 type 分支 |
| `/api/user/name` | PUT | update_user_name.php | 统一用 PUT 方法 |
| `/api/user/osu-name` | PUT | update_user_osu_name.php | 合并到 user 路由 |
| `/api/user/osu-mode` | PUT | update_user_osu_mode.py | Pydantic 枚举验证模式 |
| `/api/user/kook-id` | PUT | update_user_kook_id.php | 修正逻辑 Bug |
| `/api/user/qqguild-id` | PUT | update_user_qqguild_id.php | — |
| `/api/user/telegram-name` | PUT | update_user_telegram_name.php | — |
| `/api/user/fst-email` | PUT | update_user_fst_email.php | 邮箱格式验证 |
| `/api/user/group` | PUT | update_user_group.py | — |
| `/api/user/favorability` | PATCH | update_user_favorability.php | 增减操作用 PATCH，增加下限检查 |
| `/api/user/coin` | PATCH | update_user_coin.php | 增加下限检查 |
| `/api/user/favorability/set` | PUT | set_user_favorability.php | — |
| `/api/user/coin/set` | PUT | set_user_coin.php | — |
| `/api/user/item/use` | POST | update_use_item.php | 修正 item 存储方式，使用 JSON 字段 |
| `/api/user/item/buy` | POST | update_buy_item.php | 添加事务保护，修正类型验证 |
| `/api/user/coin/all` | GET | get_all_user_coin.php | — |
| `/api/user/check-rank` | GET | get_user_check_rank.php | 修正 is_int 验证 |

**关键优化**：
- 所有 SQL 注入 → SQLAlchemy 参数化查询
- `item` 字段改用 JSON 类型存储，不再用 `|` 替代 `"`
- `update_buy_item` 添加事务保护
- `update_user_check` 合并 type 分支，修正返回数据不一致
- `get_user_info` 合并三个查询分支为统一接口，支持 `platform` 参数

#### 2.2 回声洞模块 (`app/routers/cave.py` + `app/services/cave_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/cave/` | POST | insert_cave.php | 修正 Header 拼写错误 |
| `/api/cave/random` | GET | get_cave.php | 替换 `ORDER BY rand()` 为高效随机查询 |
| `/api/cave/{id}` | GET | select_cave.php | — |
| `/api/cave/{id}` | PUT | update_cave.py | 合并管理员/普通用户重复逻辑 |
| `/api/cave/{id}` | DELETE | delete_cave.php | — |
| `/api/cave/{id}/recover` | POST | recover_cave.php | 修正数字索引访问 |
| `/api/cave/search` | GET | random_keywords.php | 参数化查询防注入 |
| `/api/cave/upload-image` | POST | upload_image.php | 添加 URL 白名单防 SSRF |

#### 2.3 奖池/抽奖模块 (`app/routers/prize.py` + `app/services/prize_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/prize/coin` | GET | get_prize_coin.php | 修正变量未初始化问题 |
| `/api/prize/coin/rank` | GET | get_prize_coin_rank.php | 修正 is_int 验证 |
| `/api/prize/draw` | POST | insert_coins.py | 重构抽奖逻辑，添加事务保护 |
| `/api/prize/preview` | GET | preview/get_insert.php | — |
| `/api/prize/preview/old` | GET | preview/get_old.php | — |
| `/api/prize/cover` | PUT | preview/update_cover_blur.php | — |
| `/api/prize/cover/upload` | POST | preview/upload_cover.php | 添加 SSRF 防护 |
| `/api/prize/bottom/upload` | POST | preview/upload_bottom.php | 添加 SSRF 防护 |

**关键优化**：
- 抽奖逻辑重构：先发奖再扣币（或使用事务保证原子性）
- 修正 `is_int` 验证（Pydantic 自动处理类型转换）
- 图片上传添加文件类型和大小限制

#### 2.4 AI 助手模块 (`app/routers/assistant.py` + `app/services/assistant_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/assistant/deepseek/chat` | POST | DeepSeek/chat.php | 添加鉴权 |
| `/api/assistant/deepseek/reasoner` | POST | DeepSeek/reasoner.php | 合并重复代码 |
| `/api/assistant/qwen/soyo` | POST | Qwen/Nagasaki_Soyo.php | — |
| `/api/assistant/qwen/sakiko` | POST | Qwen/Togawa_Sakiko.php | 添加鉴权，统一响应格式 |

**关键优化**：
- chat.php 和 reasoner.php 合并为一个 service 方法，通过参数区分模型
- 统一 AI 对话接口抽象：`BaseAssistantService` → `DeepSeekService` / `QwenService`
- 所有接口添加鉴权
- 统一错误处理和响应格式

#### 2.5 邮件模块 (`app/routers/email.py` + `app/services/email_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/email/kirino` | POST | Kirino.php | 合并两个邮件发送逻辑 |
| `/api/email/shiruku` | POST | Shiruku.php | 合并两个邮件发送逻辑 |

**关键优化**：
- Kirino.php 和 Shiruku.php 合并为一个 `EmailService` 类，通过参数区分发件人
- 配置从环境变量读取
- 支持非 QQ 邮箱收件人
- 修正 `return` 在全局作用域无效的问题

#### 2.6 MC 模块 (`app/routers/minecraft.py` + `app/services/minecraft_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/minecraft/blacklist` | POST | blacklist/insert_user.php | 修正未定义变量 |
| `/api/minecraft/blacklist/{qq}` | GET | blacklist/get_user_info.php | 使用 ORM 字段名而非数字索引 |
| `/api/minecraft/blacklist/{id}` | DELETE | blacklist/delete_user.php | 修正字段映射错误，合并 type 分支 |
| `/api/minecraft/server` | GET | server/select_name.php | — |
| `/api/minecraft/server/by-group` | GET | server/select_qq_group.php | — |
| `/api/minecraft/ping` | GET | ping/index.php | 使用 mcstatus 库 |

**关键优化**：
- minecraft/server 目录下的文件实际操作的是 bilibili_sub 表，迁移到 RSS 路由
- 使用 `mcstatus` 库替代自写 MinecraftPing
- 修正 delete_user.php 中字段映射错位

#### 2.7 RSS/订阅模块 (`app/routers/rss.py` + `app/services/rss_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/rss/sub` | POST | RSS/add_sub.php | 修正未定义变量和表名不一致 |
| `/api/rss/sub` | DELETE | RSS/delete_sub.php | — |
| `/api/rss/sub` | PUT | RSS/update_sub.php | — |
| `/api/rss/feed` | GET | RSS/get_rss.php | — |
| `/api/rss/group` | GET | RSS/select_group.php | 参数化查询 |
| `/api/bilibili/sub` | POST | minecraft/server/add_server.php | 修正命名，移到正确位置 |
| `/api/bilibili/sub` | DELETE | minecraft/server/delete_server.php | 修正命名 |
| `/api/bilibili/sub` | PUT | minecraft/server/update_server.php | 修正命名 |

**关键优化**：
- 修正 minecraft/server 目录下文件实际操作 bilibili_sub 表的命名错误
- 修正 RSS/add_sub.php 中未定义变量和表名不一致
- 统一鉴权方式

#### 2.8 MOAuth 模块 (`app/routers/moauth.py` + `app/services/moauth_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/moauth/` | GET | get_MOAuth.php | 参数化查询，修正数字索引访问 |
| `/api/moauth/` | POST | insert_MOAuth.php | 修正频率限制逻辑，使用 secrets 模块 |
| `/api/moauth/bind-kook` | GET | MOAuth_Bind_kook.php | 参数化查询，返回 JSON 而非 HTML |

#### 2.9 百度审核模块 (`app/routers/baidu.py` + `app/services/baidu_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/baidu/img-censor` | POST | censor.php | 修正 token 刷新逻辑 |

#### 2.10 番组计划模块 (`app/routers/bangumi.py`)

| 端点 | 方法 | 原文件 |
|------|------|--------|
| `/api/bangumi/search` | POST | subject_search.php |

#### 2.11 宝塔面板模块 (`app/routers/btsoft.py` + `app/services/btsoft_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/btsoft/system-info` | GET | GetSystemInfo.php | 合并两个文件 |
| `/api/btsoft/re-memory` | POST | ReMemory.php | 合并两个文件 |

#### 2.12 同人志模块 (`app/routers/doujinshi.py`)

| 端点 | 方法 | 原文件 |
|------|------|--------|
| `/api/doujinshi/info` | GET | get_info.php |
| `/api/doujinshi/search` | GET | search.php |

#### 2.13 云盘模块 (`app/routers/myuz.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/myuz/info` | GET | get_info.php | — |
| `/api/myuz/share-info` | GET | get_share_info.php | 修正空结果处理 |

#### 2.14 osu! 模块 (`app/routers/osu.py` + `app/services/osu_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/osu/scoreboard` | GET | osu_scoreboard/index.php | 合并去重 |
| `/api/osu/signature` | GET | osu_signature/index.php | 合并去重 |

**关键优化**：
- osu_scoreboard 和 osu_signature 的 Get.php、card_*.php 完全重复，合并为统一的 `OsuService`
- 国旗图片、字体文件去重合并到 `static/` 目录
- 使用 Pillow 替代 ImageMagick

#### 2.15 统计模块 (`app/routers/statistics.py` + `app/services/statistics_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/statistics/` | POST | update_statistics.php | **禁止动态 ALTER TABLE**，改为预定义字段或 JSON 存储 |

**关键优化**：
- **最危险的接口**：原代码允许通过 API 动态修改数据库表结构，必须彻底重构
- 方案：使用 JSON 字段存储动态统计数据，或预定义所有可能的统计类型

#### 2.16 图片生成模块 (`app/routers/storm.py` + `app/services/storm_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/storm/text` | GET | storm/index.php | 添加鉴权 |
| `/api/storm/5000choyen` | GET | 5000choyen/index.php | — |
| `/api/storm/5000choyen/result` | GET | 5000choyen/result.php | 修正运算符优先级 |
| `/api/storm/5000choyen/upload` | POST | 5000choyen/setimg.php | 修正路径遍历漏洞 |
| `/api/storm/chaoshi` | GET | chaoshi/index.php | 合并重复的 break_string |
| `/api/storm/happy` | GET | happy/index.php | 合并重复的 break_string |
| `/api/storm/pw1` | GET | pw1/index.php | — |
| `/api/storm/yesno1` | GET | yesno1/index.php | — |

**关键优化**：
- 所有 `break_string` 函数合并为 `utils/image.py` 中的统一方法
- 修正 setimg.php 的路径遍历漏洞
- 修正 result.php 的运算符优先级 Bug

#### 2.17 邀请码模块 (`app/routers/invitation.py` + `app/services/invitation_service.py`)

| 端点 | 方法 | 原文件 | 优化点 |
|------|------|--------|--------|
| `/api/invitation/obtain` | POST | obtain_invitation_codes.php | 添加并发锁保护 |
| `/api/invitation/query` | GET | query_invitation_codes.py | 区分鉴权失败和查询无结果 |

---

### 阶段三：安全加固

#### 3.1 凭据管理
- 所有硬编码凭据迁移到 `.env` 文件
- `.env` 加入 `.gitignore`
- 提供 `.env.example` 模板
- `app/config.py` 使用 pydantic-settings 管理配置

#### 3.2 SQL 注入修复
- 所有数据库操作使用 SQLAlchemy ORM，自动参数化
- 禁止任何原始 SQL 拼接
- 如需原始 SQL，必须使用 `text()` + 参数绑定

#### 3.3 鉴权统一
- 所有接口统一使用 `verify_token` 依赖
- Token 从环境变量配置，不再硬编码
- 敏感操作（如管理操作）增加额外权限检查

#### 3.4 输入验证
- 所有请求参数使用 Pydantic 模型验证
- 类型、长度、格式、范围全部在模型层声明
- 不再依赖手动 `is_int()` 等检查

#### 3.5 SSRF 防护
- 图片上传/下载功能添加 URL 白名单
- 禁止访问内网 IP 地址
- 限制请求超时

#### 3.6 CORS 配置
- 配置允许的域名列表，不再使用 `*`
- 通过环境变量配置允许的源

---

### 阶段四：代码质量优化

#### 4.1 去重合并
- email/Kirino.php + Shiruku.php → `EmailService`（通过参数区分发件人）
- Assistant/DeepSeek/chat.php + reasoner.php → `DeepSeekService.chat(model=...)`
- osu_scoreboard + osu_signature 的 card_*.php → `OsuCardRenderer`
- storm 模块所有 break_string → `utils/image.py:break_string()`
- user 模块所有 update_*.php → 统一的 `UserService` 方法
- 所有 Get.php → `utils/http.py:async_get()`
- 国旗图片去重（3 份 → 1 份）
- 字体文件去重

#### 4.2 Bug 修复
- `update_buy_item.php` 中 `is_int()` 永远为 false → Pydantic 自动处理
- `get_prize_coin_rank.php` 同上
- `get_user_info.php` 逻辑分支永远不会执行 → 重构为统一查询
- `update_user_check.php` 返回数据不一致 → 使用更新后数据
- `minecraft/blacklist/delete_user.php` 字段映射错位 → 使用 ORM 字段名
- `storm/5000choyen/result.php` 运算符优先级 → 修正计算逻辑
- `statistics/update_statistics.php` 动态 ALTER TABLE → 改用 JSON 字段
- `RSS/add_sub.php` 未定义变量 → 修正
- `update_user_osu_mode.php` 运算符优先级 → 使用括号明确

#### 4.3 性能优化
- 数据库连接池（替代每次新建连接）
- `ORDER BY rand()` → 使用 `SELECT ... WHERE id >= (SELECT FLOOR(MAX(id)*RAND()) FROM cave) LIMIT 1`
- 异步 I/O（httpx 异步请求、aiosmtplib 异步邮件）
- 静态资源 CDN 或缓存头

---

### 阶段五：测试与文档

#### 5.1 测试
- 使用 pytest + pytest-asyncio
- 为每个模块编写单元测试
- 为关键业务逻辑（抽奖、签到、购买）编写集成测试
- 测试覆盖鉴权、输入验证、错误处理

#### 5.2 文档
- FastAPI 自动生成 OpenAPI/Swagger 文档
- 各端点添加描述和示例

---

## 实施优先级

1. **P0 - 基础设施**：项目初始化、配置管理、数据库层、鉴权中间件
2. **P0 - 用户模块**：最核心的模块，其他模块依赖用户数据
3. **P1 - 回声洞模块**：独立性强，可单独迁移
4. **P1 - 奖池/抽奖模块**：涉及签到卡片生成
5. **P1 - AI 助手模块**：独立性强
6. **P1 - 邮件模块**：MOAuth 依赖
7. **P2 - MC 模块**：独立性强
8. **P2 - RSS/订阅模块**：需修正命名错误
9. **P2 - MOAuth 模块**：依赖邮件模块
10. **P2 - 其他模块**：百度审核、番组计划、宝塔、同人志、云盘、osu!、统计、图片生成、邀请码
11. **P3 - 测试与文档**

---

## 注意事项

1. **数据库兼容**：新项目使用相同的数据库，确保 ORM 模型与现有表结构一致
2. **API 兼容**：保持 API 路径和参数格式兼容，方便前端/机器人端平滑迁移
3. **渐进迁移**：可以逐模块迁移，PHP 和 Python 服务并行运行
4. **静态资源**：国旗图片、字体文件等从 3 份合并为 1 份
5. **第三方库**：PHPMailer、MinecraftPing 等用 Python 等效库替代
