# NewsHub - AI驱动的新闻聚合平台

> 全自动新闻采集、AI摘要、分类推送平台

## 📖 项目概述

NewsHub 是一个基于 AI 的新闻聚合平台，自动从全球 RSS 源抓取新闻，使用 AI 进行智能摘要和分类，并通过 WebSocket 实时推送到前端展示。

**核心功能：**
- 🤖 自动抓取 47+ RSS 新闻源（10分钟一次）
- 🧠 AI智能摘要和分类（DeepSeek API）
- 📊 17个新闻分类（AI技术、机器人、芯片、汽车等）
- 🔄 WebSocket 实时推送
- 🎨 瀑布流卡片式展示
- 🎙️ AI语音播报（支持5种中文声音预设）
- 📱 响应式设计

**当前状态：**
- Token消耗：~3M tokens/天（$0.30-0.60/天）
- 新闻处理：~144次/天，约300条新闻/天
- 部署平台：Render（免费版）

---

## 🏗️ 技术栈

### 前端（Frontend）
- **框架**: React 18
- **样式**: Tailwind CSS
- **布局**: react-masonry-css（瀑布流）
- **实时通信**: Socket.IO Client
- **图标**: React Icons
- **日期**: date-fns

### 后端（Backend）
- **框架**: Express.js
- **数据库**: MongoDB（Atlas）
- **实时通信**: Socket.IO
- **缓存/消息**: Redis
- **环境**: Node.js

### AI服务（AI Service）
- **语言**: Python 3.10+
- **AI提供商**: DeepSeek API
- **爬虫**: feedparser
- **并发**: ThreadPoolExecutor（5线程）
- **调度**: schedule
- **Web服务**: Flask（健康检查）

---

## 📁 项目结构

```
news-brief-platform/
├── frontend/                 # React前端
│   ├── src/
│   │   ├── components/      # 组件
│   │   │   ├── BriefCard.js        # 新闻卡片（支持语音播报）
│   │   │   ├── CategoryFilter.js  # 分类筛选
│   │   │   └── DonateButton.js     # 打赏按钮
│   │   ├── pages/           # 页面
│   │   │   └── HomePage.js         # 主页（瀑布流+分页）
│   │   ├── services/        # API服务
│   │   │   └── api.js
│   │   ├── hooks/           # 自定义Hooks
│   │   │   └── useWebSocket.js
│   │   └── App.js
│   ├── package.json
│   └── .env                 # 环境变量（需创建）
│
├── backend/                  # Node.js后端
│   ├── src/
│   │   ├── controllers/     # 控制器
│   │   │   └── briefController.js  # 简报API
│   │   ├── models/          # 数据模型
│   │   │   └── Brief.js            # MongoDB Schema
│   │   ├── routes/          # 路由
│   │   │   └── briefRoutes.js
│   │   └── server.js        # 入口文件
│   ├── package.json
│   └── .env                 # 环境变量（需创建）
│
└── ai-service/               # Python AI服务
    ├── src/
    │   ├── crawlers/        # 爬虫
    │   │   └── news_crawler.py     # RSS爬虫
    │   ├── processors/      # AI处理
    │   │   └── cloud_ai_processor.py
    │   ├── models/          # 数据库
    │   │   └── database.py
    │   ├── filters/         # 过滤器
    │   │   └── quality_filter.py
    │   └── main.py          # 入口（调度+Flask）
    ├── config/
    │   └── settings.py      # 配置（RSS源、提示词）
    ├── requirements.txt
    └── .env                 # 环境变量（需创建）
```

---

## ⚙️ 环境配置

### 1. 克隆项目

```bash
git clone https://github.com/Luffy-D-Monkey666/news-brief-platform.git
cd news-brief-platform
```

### 2. 前端环境配置

```bash
cd frontend
npm install

# 创建 .env 文件
cat > .env << EOF
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WS_URL=http://localhost:5000
EOF
```

### 3. 后端环境配置

```bash
cd ../backend
npm install

# 创建 .env 文件
cat > .env << EOF
PORT=5000
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/news_brief?retryWrites=true&w=majority
REDIS_URL=redis://localhost:6379
CORS_ORIGIN=http://localhost:3000
EOF
```

**MongoDB配置：**
1. 注册 [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. 创建免费集群
3. 创建数据库用户
4. 添加IP白名单（0.0.0.0/0 允许所有）
5. 复制连接字符串到 `MONGODB_URI`

**Redis配置（可选）：**
- 本地开发：`brew install redis && redis-server`
- 云端：[Upstash Redis](https://upstash.com/)

### 4. AI服务环境配置

```bash
cd ../ai-service
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 创建 .env 文件
cat > .env << EOF
# DeepSeek API配置
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-deepseek-api-key
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat

# 数据库配置
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/news_brief?retryWrites=true&w=majority
REDIS_URL=redis://localhost:6379

# 爬取配置
CRAWL_INTERVAL=600  # 10分钟
AI_CONCURRENT_WORKERS=5

# 健康检查端口（Render需要）
PORT=10000
EOF
```

**获取 DeepSeek API Key：**
1. 注册 [DeepSeek](https://platform.deepseek.com/)
2. 获取 API Key
3. 充值（推荐 $10，可用1-2个月）

---

## 🚀 本地开发

### 启动顺序

**1. 启动 Redis（可选，用于实时通知）**
```bash
redis-server
```

**2. 启动后端**
```bash
cd backend
npm run dev
# 访问: http://localhost:5000
```

**3. 启动前端**
```bash
cd frontend
npm start
# 访问: http://localhost:3000
```

**4. 启动 AI 服务**
```bash
cd ai-service
source venv/bin/activate
python src/main.py
# Flask健康检查: http://localhost:10000/health
```

---

## 🌐 生产部署

### 1. Render 部署方案（当前方案）

#### Backend + Frontend（Web Service）
- **类型**: Web Service
- **构建命令**:
  ```bash
  cd backend && npm install && cd ../frontend && npm install && npm run build
  ```
- **启动命令**: `cd backend && node src/server.js`
- **环境变量**: 配置 `MONGODB_URI`, `REDIS_URL`, `CORS_ORIGIN`

#### AI Service（Web Service + Cron Job）
- **类型**: Web Service（Free）
- **构建命令**: `cd ai-service && pip install -r requirements.txt`
- **启动命令**: `cd ai-service && python src/main.py`
- **环境变量**: 配置所有 `.env` 变量
- **保持活跃**: 使用 [cron-job.org](https://cron-job.org) 每5分钟 ping `/health`

**Cron Job配置：**
1. 注册 cron-job.org
2. 创建任务：
   - URL: `https://news-platform-ai-service.onrender.com/health`
   - 间隔: 每5分钟
   - 防止 Render 休眠

### 2. 数据库
- **MongoDB**: Atlas M0（免费，512MB）
- **Redis**: Upstash（免费，10K命令/天）

---

## 📊 关键数据与优化

### Token 消耗优化历史

| 优化阶段 | Token消耗/天 | 成本/天 | 优化措施 |
|---------|-------------|---------|---------|
| **初始** | 170M | $17-34 | 无优化 |
| **第一轮** | 6.12M | $0.6-1.2 | 爬取间隔5分钟、每源10条、合并提示词、简化提示词 |
| **第二轮** | 3.06M | $0.3-0.6 | 爬取间隔10分钟（**当前**） |

**节省率：98.2%**

### 性能优化（最新）

**前端优化：**
- 初始加载：50条 → 30条（减少40%数据传输）
- React Hooks优化（useCallback）
- 内存泄漏修复（setTimeout cleanup）

**后端优化：**
- 所有查询添加 `.lean()`（性能提升30%）
- 复合索引：`{ category: 1, created_at: -1 }`
- API响应时间减少30%

---

## 📡 API文档

### 后端API

**Base URL**: `http://localhost:5000/api` (本地) 或 `https://your-app.onrender.com/api` (生产)

#### 1. 获取最新简报
```http
GET /briefs/latest?category={category}&limit={limit}
```
- **参数**:
  - `category` (可选): 分类过滤
  - `limit` (可选): 数量限制，默认20
- **响应**:
  ```json
  {
    "success": true,
    "count": 30,
    "data": [...]
  }
  ```

#### 2. 获取历史简报（分页）
```http
GET /briefs/history?category={category}&page={page}&limit={limit}
```
- **参数**:
  - `category` (可选): 分类过滤
  - `page` (可选): 页码，默认1
  - `limit` (可选): 每页数量，默认20
- **响应**:
  ```json
  {
    "success": true,
    "data": [...],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "pages": 8
    }
  }
  ```

#### 3. 获取简报详情
```http
GET /briefs/:id
```
- **响应**:
  ```json
  {
    "success": true,
    "data": {
      "_id": "...",
      "title": "...",
      "summary": "...",
      "category": "...",
      ...
    }
  }
  ```

#### 4. 分类统计
```http
GET /briefs/stats/category
```
- **响应**:
  ```json
  {
    "success": true,
    "data": [
      {
        "_id": "ai_technology",
        "count": 45,
        "latest": "2024-01-15T..."
      }
    ]
  }
  ```

### WebSocket 事件

**连接**: `http://localhost:5000`

**事件**:
- `news:new` - 新简报推送
  ```javascript
  socket.on('news:new', (brief) => {
    console.log('新简报:', brief);
  });
  ```

---

## 🎯 17个新闻分类

| 代码 | 名称 | 说明 |
|------|------|------|
| `ai_technology` | AI技术 | 机器学习、大语言模型、AI应用 |
| `robotics` | 机器人 | 工业/服务/人形机器人、自动驾驶 |
| `ai_programming` | AI编程 | AI编程助手、开发工具、开源项目 |
| `semiconductors` | 芯片半导体 | 芯片设计、制造、设备、材料 |
| `opcg` | OPCG卡牌 | One Piece Card Game |
| `automotive` | 汽车 | 电动车/燃油车、充电桩、电池 |
| `consumer_electronics` | 消费电子 | 手机、手表、眼镜、相机、无人机 |
| `one_piece` | ONE PIECE | 海贼王动漫周边 |
| `podcasts` | 播客推荐 | 优质播客节目内容推荐 |
| `finance_investment` | 投资财经 | 股票、基金、投资 |
| `business_tech` | 商业科技 | 科技公司、商业模式 |
| `politics_world` | 政治国际 | 国际政治、外交 |
| `economy_policy` | 经济政策 | 宏观经济、政策 |
| `health_medical` | 健康医疗 | 医疗、健康、生物科技 |
| `energy_environment` | 能源环境 | 新能源、环保 |
| `entertainment_sports` | 娱乐体育 | 娱乐、体育 |
| `general` | 综合 | 其他新闻 |

---

## 🔧 常见问题

### 1. MongoDB 连接失败
- 检查 IP 白名单（添加 0.0.0.0/0）
- 检查用户名密码
- 确认连接字符串格式正确

### 2. AI Service Token消耗过快
- 检查 `CRAWL_INTERVAL`（当前600秒）
- 检查 RSS 源数量（当前47个）
- 每源抓取数量（当前10条）

### 3. Render 服务休眠
- 确保 Cron Job 正常运行（每5分钟 ping `/health`）
- 检查 Render 日志

### 4. 前端刷新慢
- 已优化：初始加载30条、`.lean()` 查询、复合索引
- 如仍慢，检查网络或数据库连接

### 5. Redis 连接失败
- Redis 是可选的，仅用于实时推送
- 如无 Redis，系统仍可正常运行（无实时通知）

---

## 📝 开发规范

### Git 提交规范
```bash
# 功能
feat: 添加新功能

# 修复
fix: 修复bug

# 优化
perf: 性能优化

# 文档
docs: 更新文档

# 样式
style: 代码格式调整
```

### 代码风格
- **前端**: ESLint + Prettier
- **后端**: ESLint
- **Python**: PEP 8

---

## 📈 监控与日志

### AI Service 日志格式
```
2024-01-15 10:00:00 - INFO - ==========================================
2024-01-15 10:00:00 - INFO - 开始新一轮新闻采集
2024-01-15 10:00:00 - INFO - 步骤 1/5: 开始爬取 RSS 订阅源...
2024-01-15 10:00:15 - INFO - 步骤 1/5 完成: 爬取到 470 条新闻
2024-01-15 10:00:15 - INFO - 步骤 2/5: 批量过滤重复新闻...
2024-01-15 10:00:20 - INFO - 步骤 2/5 完成: 过滤后剩余 30 条新新闻
2024-01-15 10:00:20 - INFO - 步骤 2.5/5: 内容质量过滤...
2024-01-15 10:00:20 - INFO - 步骤 2.5/5 完成: 所有内容通过质量检查
2024-01-15 10:00:20 - INFO - 步骤 3/5: 保存原始新闻到数据库...
2024-01-15 10:00:25 - INFO - 步骤 3/5 完成: 已保存 30 条原始新闻
2024-01-15 10:00:25 - INFO - 步骤 4/5: 开始 AI 处理 (30 条新闻)...
2024-01-15 10:00:25 - INFO - Token优化: 使用合并提示词，一次调用完成摘要+分类
2024-01-15 10:02:30 - INFO - 步骤 4/5 完成: AI 处理完成，生成 30 条简报
2024-01-15 10:02:30 - INFO - 步骤 5/5: 保存简报到数据库...
2024-01-15 10:02:35 - INFO - 步骤 5/5 完成: 成功保存 30/30 条简报
2024-01-15 10:02:35 - INFO - 本轮采集完成，耗时 155.0 秒
2024-01-15 10:02:35 - INFO - ==========================================
```

---

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📄 许可证

MIT License

---

## 📞 联系方式

- **项目仓库**: https://github.com/Luffy-D-Monkey666/news-brief-platform
- **问题反馈**: [GitHub Issues](https://github.com/Luffy-D-Monkey666/news-brief-platform/issues)

---

## 🎉 致谢

- **AI提供商**: DeepSeek
- **部署平台**: Render
- **数据库**: MongoDB Atlas
- **图标**: React Icons
- **布局**: Masonry Layout

---

*最后更新: 2024-02-06*
