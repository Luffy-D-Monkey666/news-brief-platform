# NewsHub - AI新闻聚合平台

一个基于AI的实时新闻聚合和简报系统，支持多分类新闻自动提炼、结构化展示和实时推送。

## 🌐 在线体验

- **前端**: https://news-frontend-e14o.onrender.com
- **API**: https://news-backend-rp9y.onrender.com

> ⚠️ 免费版 Render 会休眠，首次访问可能需要等待 30-50 秒唤醒

---

## ✨ 功能特性

### 核心功能
- ✅ **70+全球新闻源** - 覆盖AI、机器人、芯片、汽车、财经等18个分类
- ✅ **AI智能提炼** - DeepSeek驱动，自动生成结构化简报
- ✅ **三段式简报** - 事件概述 → 重要细节 → 后续影响
- ✅ **实时推送** - WebSocket，无需刷新
- ✅ **时间筛选** - 1小时内/今日/本周
- ✅ **双视图模式** - 卡片瀑布流/列表视图
- ✅ **语音朗读** - 5种中文语音预设

### 新闻分类（18个）
| 核心科技 | 主流新闻 | 兴趣领域 |
|---------|---------|---------|
| AI技术 | 商业科技 | 动漫二次元 |
| 机器人 | 政治国际 | 海贼王(OP) |
| AI编程 | 经济政策 | TCG卡牌 |
| 芯片半导体 | 健康医疗 | |
| 汽车 | 能源环境 | |
| 消费电子 | 娱乐体育 | |
| 播客推荐 | 投资财经 | |

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│         Tailwind CSS + Socket.io + Masonry                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (Node.js)                          │
│            Express + MongoDB + Redis + Socket.io            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  AI Service (Python)                         │
│         RSS Crawler → DeepSeek API → 结构化简报             │
└─────────────────────────────────────────────────────────────┘
```

| 层级 | 技术 |
|-----|------|
| 前端 | React 18, Tailwind CSS, Socket.io-client, react-masonry-css |
| 后端 | Node.js 18+, Express, MongoDB, Redis, Socket.io |
| AI服务 | Python 3.9+, DeepSeek API, Feedparser, BeautifulSoup4 |
| 部署 | Docker, Render/Railway/Vercel |

---

## 🚀 快速开始

### 方式一：云端部署（推荐）

1. Fork 本项目到你的 GitHub
2. 在 [Render](https://render.com) 创建账号
3. 参考 [`CLOUD_DEPLOY.md`](./CLOUD_DEPLOY.md) 配置
4. 连接 [MongoDB Atlas](https://www.mongodb.com/atlas)（免费版够用）

### 方式二：本地开发

#### 前置要求
- Node.js 18+
- Python 3.9+
- MongoDB 6+（或使用 MongoDB Atlas）
- Redis 7+（或使用 Upstash）

#### 步骤

```bash
# 1. 克隆项目
git clone https://github.com/Luffy-D-Monkey666/news-brief-platform.git
cd news-brief-platform

# 2. 启动依赖服务（可选，也可用云端服务）
docker run -d -p 27017:27017 --name mongo mongo:6
docker run -d -p 6379:6379 --name redis redis:7

# 3. 配置环境变量
cp ai-service/.env.example ai-service/.env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# 编辑 .env 文件填入实际值（见下方说明）

# 4. 启动 AI 服务
cd ai-service
pip install -r requirements.txt
python src/main.py &

# 5. 启动后端
cd ../backend
npm install
npm run dev &

# 6. 启动前端
cd ../frontend
npm install
npm start
```

#### 环境变量配置

**ai-service/.env**
```bash
# DeepSeek API（必填）
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# MongoDB（必填）
MONGODB_URI=mongodb://localhost:27017/newshub
# 或 Atlas: mongodb+srv://user:pass@cluster.xxxxx.mongodb.net/newshub

# 可选配置
CRAWL_INTERVAL=120  # 爬取间隔（秒）
```

**backend/.env**
```bash
PORT=5000
MONGODB_URI=mongodb://localhost:27017/newshub
REDIS_URL=redis://localhost:6379
```

**frontend/.env**
```bash
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WS_URL=http://localhost:5000
```

---

## 📡 API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/briefs/latest?category=xxx&limit=50` | 获取最新简报 |
| GET | `/api/briefs/history?page=1&limit=20` | 分页获取历史 |
| GET | `/api/briefs/stats` | 分类统计 |
| GET | `/api/briefs/:id` | 简报详情 |

### WebSocket 事件
```javascript
// 连接
const socket = io('http://localhost:5000');

// 监听新简报
socket.on('news:update', (brief) => {
  console.log('新简报:', brief);
});
```

### 响应示例
```json
{
  "success": true,
  "count": 1,
  "data": [{
    "_id": "xxx",
    "title": "OpenAI发布GPT-5",
    "summary": "事件概述: ...\n\n重要细节:\n• ...\n\n后续影响: ...",
    "category": "ai_technology",
    "source": "OpenAI Blog",
    "link": "https://...",
    "image": "https://...",
    "published": "2026-02-18T12:00:00Z",
    "created_at": "2026-02-18T12:05:00Z"
  }]
}
```

---

## 📖 简报结构

每条新闻简报包含三个层次：

```
📰 标题（中文，≤30字）

🔵 事件概述
   1-2句话说清楚发生了什么

🟡 重要细节（3-5条）
   • 关键数据/人物/时间
   • 技术细节/产品规格
   • 涉及的公司/机构
   • 官方说法或权威引用

🟢 后续影响
   对行业/市场/用户的意义
   后续可能的发展方向
```

---

## 🗺️ 路线图

### ✅ 已完成
- [x] 三段式结构化简报
- [x] 时间筛选器
- [x] 列表/卡片视图切换
- [x] 语音朗读功能
- [x] 70+ 优质新闻源

### 🔜 规划中

| 优先级 | 功能 | 说明 |
|--------|------|------|
| P0 | 原文关键引用 | 保留1-2句原文金句 |
| P0 | 来源可信度标识 | 官方/权威媒体/社区分级 |
| P0 | Breaking News | 重要新闻标签+置顶 |
| P1 | 行动建议 | 商业新闻增加风险提示 |
| P1 | 关键数字提取 | 自动提取并与历史对比 |
| P2 | 话题聚合 | 同一事件多篇报道聚合 |
| P2 | 背景知识 | 重大事件关联历史背景 |

> 📋 详细设计文档见 [`docs/ROADMAP.md`](./docs/ROADMAP.md)

---

## 🐛 常见问题

### AI Service 长时间没有新新闻
1. Render 免费版 Worker 会休眠，访问前端会自动唤醒
2. 检查 Render Dashboard → AI Service → Logs 是否有错误
3. 确认 `DEEPSEEK_API_KEY` 环境变量正确

### 简报只显示一句话，没有三段式结构
- 只有新抓取的新闻才会用新格式
- 旧数据需要清空 MongoDB 重新抓取
- 或等待新新闻自动进入

### 本地启动报错 MongoDB 连接失败
```bash
# 确保 MongoDB 正在运行
docker ps | grep mongo
# 如果没有，启动它
docker run -d -p 27017:27017 --name mongo mongo:6
```

### 前端显示 "加载中..." 不消失
- 后端可能没启动或休眠中
- 检查浏览器控制台是否有 CORS 错误
- 确认 `REACT_APP_API_URL` 配置正确

---

## 📁 项目结构

```
news-brief-platform/
├── ai-service/           # Python AI服务
│   ├── src/
│   │   ├── crawlers/     # RSS新闻爬虫
│   │   ├── processors/   # AI处理器（DeepSeek）
│   │   └── models/       # 数据模型
│   └── config/           # 新闻源、提示词配置
├── backend/              # Node.js 后端
│   └── src/
│       ├── controllers/  # API控制器
│       ├── models/       # MongoDB模型
│       └── routes/       # 路由定义
├── frontend/             # React 前端
│   └── src/
│       ├── components/   # UI组件
│       ├── pages/        # 页面
│       └── hooks/        # 自定义Hooks
└── docs/                 # 文档
```

---

## 🤝 贡献指南

### 开发流程
1. Fork 本项目
2. 创建功能分支：`git checkout -b feature/xxx`
3. 提交更改：`git commit -m "feat: 添加xxx功能"`
4. 推送分支：`git push origin feature/xxx`
5. 创建 Pull Request

### 提交规范
遵循 [Conventional Commits](https://www.conventionalcommits.org/)：
- `feat:` 新功能
- `fix:` 修复Bug
- `docs:` 文档更新
- `refactor:` 重构
- `style:` 样式调整

### 代码规范
- **前端**: ESLint + Prettier
- **Python**: Black + isort
- **提交前**: 确保 `npm run lint` 和 `black .` 通过

---

## 📄 许可证

MIT License

---

**NewsHub** - 让新闻阅读更高效 📰
