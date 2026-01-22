# 实时新闻简报平台

一个基于开源AI模型的实时新闻聚合和简报系统，支持多分类新闻自动提炼和实时推送。

## 功能特性

- ✅ 全网新闻实时抓取
- ✅ AI智能提炼和分类（财经、科技、健康、新能源、汽车、机器人、AI等）
- ✅ WebSocket实时推送
- ✅ 新闻来源追溯
- ✅ 响应式Web界面

## 技术栈

### 后端
- Node.js + Express (API服务)
- MongoDB (数据存储)
- Redis (缓存和消息队列)
- Socket.io (WebSocket实时通信)

### AI服务
- Python 3.9+
- Ollama (本地开源LLM运行环境)
- Llama 3 / Qwen 2 (新闻提炼和分类)
- Feedparser (RSS订阅)
- BeautifulSoup4 (网页解析)

### 前端
- React 18 + TypeScript
- Tailwind CSS
- Socket.io-client
- Axios

## 快速开始

### 前置要求

- Node.js 18+
- Python 3.9+
- MongoDB 6+
- Redis 7+
- Docker & Docker Compose (推荐)

### 使用Docker部署（推荐）

```bash
# 克隆项目
git clone <your-repo>
cd news-brief-platform

# 启动所有服务
docker-compose up -d

# 访问应用
# 前端: http://localhost:3000
# 后端API: http://localhost:5000
```

### 手动部署

#### 1. 安装Ollama和模型

```bash
# 安装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取Llama 3模型
ollama pull llama3

# 或使用Qwen 2（中文效果更好）
ollama pull qwen2:7b
```

#### 2. 启动AI服务

```bash
cd ai-service
pip install -r requirements.txt
python src/main.py
```

#### 3. 启动后端服务

```bash
cd backend
npm install
npm run dev
```

#### 4. 启动前端服务

```bash
cd frontend
npm install
npm start
```

## 环境变量配置

### backend/.env
```
PORT=5000
MONGODB_URI=mongodb://localhost:27017/news-brief
REDIS_URL=redis://localhost:6379
AI_SERVICE_URL=http://localhost:8000
```

### ai-service/.env
```
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=llama3
CRAWL_INTERVAL=300
```

### frontend/.env
```
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WS_URL=ws://localhost:5000
```

## 项目结构

```
news-brief-platform/
├── backend/              # Node.js后端服务
│   ├── src/
│   │   ├── controllers/  # 控制器
│   │   ├── models/       # 数据模型
│   │   ├── routes/       # 路由
│   │   ├── services/     # 业务逻辑
│   │   └── middleware/   # 中间件
│   └── config/           # 配置文件
├── ai-service/           # Python AI服务
│   ├── src/
│   │   ├── crawlers/     # 新闻爬虫
│   │   ├── processors/   # AI处理器
│   │   └── models/       # 数据模型
│   └── config/           # 配置文件
├── frontend/             # React前端
│   ├── src/
│   │   ├── components/   # UI组件
│   │   ├── pages/        # 页面
│   │   ├── hooks/        # 自定义Hooks
│   │   └── services/     # API服务
│   └── public/           # 静态资源
└── docker-compose.yml    # Docker编排
```

## API文档

### 获取最新简报
```
GET /api/briefs/latest?category=tech
```

### 获取历史简报
```
GET /api/briefs/history?page=1&limit=20
```

### WebSocket事件
- `news:update` - 新简报推送
- `category:update` - 分类更新

## 开发计划

- [ ] 添加用户订阅功能
- [ ] 邮件/推送通知
- [ ] 自定义新闻源
- [ ] 多语言支持
- [ ] 数据可视化

## 许可证

MIT License
