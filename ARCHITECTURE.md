# 系统架构文档

## 系统概述

实时新闻简报平台是一个基于开源AI模型的全自动新闻聚合和提炼系统，能够从全网实时抓取新闻，使用AI进行智能摘要和分类，并通过WebSocket实时推送到前端展示。

## 技术架构

### 整体架构图

```
┌─────────────┐
│   用户浏览器   │
└──────┬──────┘
       │ HTTP/WebSocket
       ▼
┌─────────────────────────────────────┐
│          前端 (React)                │
│  - 响应式UI                          │
│  - WebSocket实时通信                 │
│  - 分类筛选                          │
└──────┬──────────────────────────────┘
       │ REST API / WebSocket
       ▼
┌─────────────────────────────────────┐
│       后端 (Node.js + Express)       │
│  - RESTful API                       │
│  - WebSocket服务器                   │
│  - 数据查询和管理                     │
└──────┬───────────┬──────────────────┘
       │           │
       │           │ Redis Pub/Sub
       │           ▼
       │    ┌─────────────┐
       │    │    Redis    │
       │    │  消息队列     │
       │    └──────▲──────┘
       │           │
       │           │ Publish
       │           │
       │    ┌──────┴──────────────────┐
       │    │   AI服务 (Python)        │
       │    │  - 新闻爬虫              │
       │    │  - Ollama AI处理         │
       │    │  - 新闻提炼和分类         │
       │    └─────────────────────────┘
       │           │
       │           │ Local HTTP
       │           ▼
       │    ┌─────────────┐
       │    │   Ollama    │
       │    │  开源LLM引擎  │
       │    │ (Qwen2/Llama)│
       │    └─────────────┘
       │
       ▼
┌─────────────┐
│   MongoDB   │
│  数据持久化   │
└─────────────┘
```

## 核心模块

### 1. AI服务 (Python)

**职责**: 新闻采集、AI处理、数据存储

**核心组件**:

#### 新闻爬虫 (news_crawler.py)
- RSS订阅源聚合
- 支持多种新闻格式
- 自动去重
- 定时调度

#### AI处理器 (ai_processor.py)
- 支持多种云端AI: Kimi(Moonshot), DeepSeek, OpenAI, Claude
- 新闻摘要生成（50-100字）
- 智能分类（17个类别）
- 批量处理优化

#### 数据模型 (database.py)
- MongoDB操作封装
- 原始新闻存储
- 简报管理
- 索引优化

**工作流程**:
```
1. 定时爬取新闻 (5分钟间隔)
2. 去重检查
3. AI摘要生成
4. 智能分类
5. 存入MongoDB
6. 发布到Redis
```

### 2. 后端服务 (Node.js)

**职责**: API服务、WebSocket通信、业务逻辑

**核心组件**:

#### API路由 (routes/)
- `GET /api/briefs/latest` - 获取最新简报
- `GET /api/briefs/history` - 获取历史简报（分页）
- `GET /api/briefs/stats` - 获取分类统计
- `GET /api/briefs/:id` - 获取简报详情
- `GET /health` - 健康检查

#### WebSocket服务 (websocketService.js)
- Socket.io实现
- Redis订阅监听
- 房间管理（分类订阅）
- 实时广播

**特性**:
- CORS支持
- 错误处理中间件
- 安全性增强（Helmet）
- 请求日志（Morgan）

### 3. 前端应用 (React)

**职责**: 用户界面、实时更新、交互体验

**核心组件**:

#### 页面 (pages/)
- HomePage - 主页面，展示简报流

#### 组件 (components/)
- BriefCard - 简报卡片
  - 分类标签
  - 时间显示
  - 来源信息
  - 原文链接
- CategoryFilter - 分类筛选器
  - 8个分类选择
  - 图标展示
  - 实时切换

#### Hooks (hooks/)
- useWebSocket - WebSocket连接管理
  - 自动重连
  - 连接状态
  - 消息监听

#### 服务 (services/)
- api.js - HTTP请求封装
  - Axios实例
  - 拦截器
  - 错误处理

**特性**:
- 响应式设计（Tailwind CSS）
- 实时更新动画
- 新消息标记
- 分类筛选
- 无限加载

## 数据流

### 新闻采集流程

```
RSS源 → 爬虫 → 去重 → 原始新闻存储(MongoDB)
                ↓
              AI处理
                ↓
         ┌──────┴──────┐
         ▼             ▼
      摘要生成       智能分类
         └──────┬──────┘
                ▼
         简报存储(MongoDB)
                ▼
         发布到Redis
```

### 实时推送流程

```
AI服务 → Redis Pub → 后端订阅 → WebSocket → 前端更新
                                    ↓
                              ┌─────┴─────┐
                              ▼           ▼
                          全局广播    分类房间
```

### API查询流程

```
前端请求 → 后端API → MongoDB查询 → 数据返回 → 前端渲染
```

## 数据模型

### MongoDB Collections

#### news（原始新闻）
```javascript
{
  _id: ObjectId,
  title: String,           // 标题
  content: String,         // 内容
  link: String (unique),   // 链接
  source: String,          // 来源
  source_url: String,      // 来源URL
  published: Date,         // 发布时间
  created_at: Date         // 创建时间
}
```

#### briefs（简报）
```javascript
{
  _id: ObjectId,
  title: String,           // 标题
  summary: String,         // AI摘要
  category: String,        // 分类
  source: String,          // 来源
  source_url: String,      // 来源URL
  link: String,            // 原文链接
  published: Date,         // 发布时间
  created_at: Date,        // 创建时间
  is_pushed: Boolean,      // 是否已推送
  pushed_at: Date          // 推送时间
}
```

### Redis Channels

- `news:new` - 新简报发布频道

## AI提示词设计

### 摘要提示词
```
请分析以下新闻内容，提炼成一条简洁的新闻简报（50-100字）。
要求：
1. 保留最核心的信息
2. 使用简洁专业的语言
3. 突出新闻价值和影响
```

### 分类提示词
```
请将以下新闻分类到最合适的类别中。
可选类别：财经、科技、健康、新能源、汽车、机器人、AI、综合
只返回类别英文名称，不要其他内容。
```

## 分类系统

| 分类 | 英文标识 | 颜色 | 图标 | 说明 |
|------|---------|------|------|------|
| 财经 | finance | 绿色 | 💵 | 金融、经济、市场 |
| 科技 | technology | 蓝色 | 💻 | 通用科技新闻 |
| 健康 | health | 红色 | ❤️ | 医疗、健康、生物 |
| 新能源 | new_energy | 黄色 | 🍃 | 可再生能源、环保 |
| 汽车 | automotive | 紫色 | 🚗 | 汽车行业、交通 |
| 机器人 | robotics | 靛蓝 | 🤖 | 机器人技术 |
| AI | ai | 粉色 | 🧠 | 人工智能 |
| 综合 | general | 灰色 | 🌐 | 其他类别 |

## 性能优化

### AI服务优化
- 批量处理新闻
- 模型参数调优（temperature=0.3）
- 内容长度限制
- 异常处理和重试

### 后端优化
- MongoDB索引优化
- Redis缓存策略
- WebSocket房间管理
- 连接池配置

### 前端优化
- 组件懒加载
- 虚拟滚动（未来实现）
- 请求防抖
- 状态管理优化

## 扩展性设计

### 新增新闻源
编辑 `ai-service/config/settings.py`:
```python
NEWS_SOURCES = {
    'rss_feeds': [
        'https://new-source.com/feed',
    ]
}
```

### 新增分类
1. 修改 `ai-service/config/settings.py` 的 `CATEGORIES`
2. 更新前端 `categoryNames` 和 `categoryIcons`
3. 调整AI分类提示词

### 自定义提示词
修改 `ai-service/config/settings.py`:
```python
SUMMARIZE_PROMPT = "你的自定义提示词..."
```

## 安全考虑

- CORS限制
- 输入验证
- XSS防护（React自动转义）
- SQL注入防护（MongoDB参数化查询）
- 速率限制（未来实现）
- 身份认证（未来实现）

## 监控和日志

### 日志系统
- Python: logging模块
- Node.js: Morgan + console
- 日志级别: INFO, ERROR, DEBUG

### 监控指标
- 新闻采集数量
- AI处理成功率
- WebSocket连接数
- API响应时间
- 数据库查询性能

## 部署方案

### Docker部署（推荐）
- 使用docker-compose
- 服务隔离
- 资源限制
- 健康检查

### 手动部署
- 进程管理（PM2）
- Nginx反向代理
- SSL证书配置
- 日志轮转

## 未来规划

- [ ] 用户系统和个性化订阅
- [ ] 邮件/推送通知
- [ ] 数据可视化统计
- [ ] 多语言支持
- [ ] 移动端适配
- [ ] 高级搜索功能
- [ ] 新闻情感分析
- [ ] 趋势预测
