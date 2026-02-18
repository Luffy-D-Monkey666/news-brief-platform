# NewsHub - AI新闻聚合平台

一个基于AI的实时新闻聚合和简报系统，支持多分类新闻自动提炼、结构化展示和实时推送。

## ✨ 功能特性

### 核心功能
- ✅ **70+全球新闻源实时抓取** - 覆盖AI、机器人、芯片、汽车、财经等18个分类
- ✅ **AI智能提炼** - DeepSeek驱动，自动生成结构化简报
- ✅ **三段式简报结构** - 事件概述 → 重要细节 → 后续影响
- ✅ **WebSocket实时推送** - 新闻实时更新，无需刷新页面
- ✅ **新闻来源追溯** - 一键跳转原文

### v2.0 新增功能
- ✅ **时间筛选器** - 支持"1小时内"/"今日"/"本周"快速筛选
- ✅ **双视图模式** - 卡片瀑布流 / 列表紧凑视图自由切换
- ✅ **语音朗读** - 5种中文语音预设（Siri/小爱/理想同学/NOMI）
- ✅ **按时间排序** - 最新新闻始终在前

### 新闻分类（18个）
| 核心科技 | 主流新闻 | 兴趣领域 |
|---------|---------|---------|
| AI技术 | 商业科技 | 动漫二次元 |
| 机器人 | 政治国际 | 海贼王(OP) |
| AI编程 | 经济政策 | TCG卡牌 |
| 芯片半导体 | 健康医疗 | |
| 汽车 | 能源环境 | |
| 消费电子 | 娱乐体育 | |
| 播客推荐 | | |
| 投资财经 | | |

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│    React 18 + Tailwind CSS + Socket.io + Masonry            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Backend (Node.js)                       │
│         Express + MongoDB + Redis + Socket.io               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Service (Python)                       │
│    RSS Crawler → DeepSeek API → 结构化简报生成              │
└─────────────────────────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术 |
|-----|------|
| 前端 | React 18, Tailwind CSS, Socket.io-client, react-masonry-css |
| 后端 | Node.js, Express, MongoDB, Redis, Socket.io |
| AI服务 | Python 3.9+, DeepSeek API, Feedparser, BeautifulSoup4 |
| 部署 | Docker, Render/Railway/Vercel |

## 🚀 快速开始

### 云端部署（推荐）

项目支持一键部署到 Render/Railway：

1. Fork 本项目
2. 参考 `CLOUD_DEPLOY.md` 配置环境变量
3. 连接 MongoDB Atlas
4. 部署完成！

### 本地开发

```bash
# 克隆项目
git clone https://github.com/Luffy-D-Monkey666/news-brief-platform.git
cd news-brief-platform

# 使用 Docker Compose（推荐）
docker-compose up -d

# 或手动启动各服务
# 1. AI服务
cd ai-service && pip install -r requirements.txt && python src/main.py

# 2. 后端
cd backend && npm install && npm run dev

# 3. 前端
cd frontend && npm install && npm start
```

### 环境变量

```bash
# AI服务 (.env)
DEEPSEEK_API_KEY=your_deepseek_key
MONGODB_URI=mongodb://...

# 后端 (.env)
MONGODB_URI=mongodb://...
REDIS_URL=redis://...

# 前端 (.env)
REACT_APP_API_URL=http://localhost:5000
```

## 📖 简报结构说明

每条新闻简报包含三个层次：

```
📰 标题（中文，≤30字）

🔵 事件概述
   1-2句话说清楚"发生了什么"

🟡 重要细节（3-5条要点）
   • 关键数据/人物/时间
   • 技术细节/产品规格
   • 涉及的公司/机构
   • 官方说法或权威引用

🟢 后续影响
   这件事对行业/市场/用户意味着什么？
   后续可能的发展方向
```

## 🗺️ 路线图

### 已完成 ✅
- [x] 三段式结构化简报
- [x] 时间筛选器
- [x] 列表/卡片视图切换
- [x] 语音朗读功能
- [x] 70+ 优质新闻源

### 计划中 🔜
- [ ] 话题聚合 - 相关新闻自动关联
- [ ] 原文关键引用 - 保留1-2句原文
- [ ] Breaking News标签 - 紧急/重要新闻高亮
- [ ] 来源可信度标识 - 官方/非官方来源区分
- [ ] 数据对比 - 关键数字与历史对比
- [ ] 行动建议 - 针对管理者的风险提示
- [ ] 定制化订阅 - 关注特定公司/领域
- [ ] 一键分享 - 生成摘要卡片

## 📁 项目结构

```
news-brief-platform/
├── ai-service/           # Python AI服务
│   ├── src/
│   │   ├── crawlers/     # RSS新闻爬虫
│   │   ├── processors/   # AI处理器（DeepSeek）
│   │   └── models/       # 数据模型
│   └── config/           # 配置（新闻源、提示词）
├── backend/              # Node.js后端
│   └── src/
│       ├── controllers/  # API控制器
│       ├── models/       # MongoDB模型
│       └── routes/       # 路由定义
├── frontend/             # React前端
│   └── src/
│       ├── components/   # UI组件（BriefCard等）
│       ├── pages/        # 页面（HomePage）
│       └── hooks/        # WebSocket等Hooks
└── docs/                 # 部署文档
```

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 许可证

MIT License

---

**NewsHub** - 让新闻阅读更高效 📰
