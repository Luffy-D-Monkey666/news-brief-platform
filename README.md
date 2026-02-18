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
- ✅ **三段式简报** - 事件概述 → 原文引用 → 重要细节 → 后续影响
- ✅ **实时推送** - WebSocket，无需刷新
- ✅ **时间筛选** - 1小时内/今日/本周
- ✅ **三种视图** - 卡片瀑布流/列表/话题聚合
- ✅ **语音朗读** - 5种中文语音预设

### v2.0 新增功能（2026-02-18）
- ✅ **原文关键引用** - 保留1-2句原文金句
- ✅ **来源可信度标识** - 🏛️官方/📰权威/🔬专业/💬社区 四级分类
- ✅ **Breaking News** - 重要新闻红色高亮+边框
- ✅ **行动建议** - 财经类新闻显示风险提示和行动建议
- ✅ **关键数字提取** - 自动提取营收/用户数等关键指标
- ✅ **背景知识+时间线** - 重要新闻显示背景介绍和事件发展历程
- ✅ **话题聚合** - 同一事件多篇报道自动归类，话题视图展示

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

## 📖 简报结构

每条新闻简报包含以下层次：

```
📰 标题（中文，≤30字）

🏛️/📰/🔬/💬 来源可信度标签

🔵 事件概述
   1-2句话说清楚发生了什么

💬 原文引用
   "关键原文引用" — 说话人

🟡 重要细节（3-5条）
   • 关键数据/人物/时间
   • 技术细节/产品规格
   • 涉及的公司/机构

🟢 后续影响
   对行业/市场/用户的意义

📊 关键数据（如有）
   营收: $50B | 增长: +15%

📚 背景知识（重要新闻）
   公司/人物背景 + 事件时间线

⚠️ 行动建议（财经类）
   风险提示 + 操作建议
```

---

## 🗺️ 路线图

### ✅ 已完成

#### 基础功能
- [x] 三段式结构化简报
- [x] 时间筛选器（1小时/今日/本周）
- [x] 列表/卡片视图切换
- [x] 语音朗读功能（5种语音）
- [x] 70+ 优质新闻源

#### v2.0 内容增强
- [x] 原文关键引用
- [x] 来源可信度标识（官方/权威/专业/社区）
- [x] Breaking News 重要新闻高亮
- [x] 行动建议/风险提示（财经类）
- [x] 关键数字提取
- [x] 背景知识 + 事件时间线
- [x] 话题聚合 + 话题视图

---

### 🔜 规划中

#### 第四阶段：个性化与深度内容

| 优先级 | 功能 | 说明 | 状态 |
|--------|------|------|------|
| 🥇 | **技术解读段落** | AI/芯片/机器人类新闻增加技术原理分析 | ⏳ 待开发 |
| 🥇 | **机器人公司追踪** | Tesla Bot/宇树/智元等重点公司动态聚合 | ⏳ 待开发 |
| 🥈 | **语音早报（TTS）** | 每日自动生成语音版新闻摘要 | ⏳ 待开发 |
| 🥈 | **股票数据补充** | 上市公司自动补充市值、PE、涨跌幅 | ⏳ 待开发 |
| 🥈 | **融资历史** | 融资新闻显示该公司历史融资记录 | ⏳ 待开发 |
| 🥉 | **个性化首页** | 根据用户关注领域生成「我的日报」 | ⏳ 待开发 |
| 🥉 | **OPCG独立分类** | 海贼王卡牌从TCG中独立 | ⏳ 待开发 |

#### 详细设计

**技术解读段落**
```
🔬 技术解读:
GPT-5采用MoE架构，将参数量扩展至万亿级别同时保持推理效率。
相比GPT-4，主要改进在长上下文理解和多模态融合。
技术成熟度：已进入商用阶段。
```
- 适用分类：ai_technology, robotics, ai_programming, semiconductors
- 实现方式：修改AI提示词
- 工作量：0.5天

**语音早报（TTS）**
```
🎧 今日早报（5分钟）
1. OpenAI发布GPT-5...
2. 特斯拉机器人量产...
3. 美联储维持利率...
[播放] [下载]
```
- 技术方案：Azure TTS API
- 成本：约¥0.01/千字
- 工作量：2-3天

**股票数据补充**
```
📈 股票信息:
特斯拉 (TSLA) | 市值: $8000亿 | PE: 65 | 今日: +2.3%
```
- 数据源：Yahoo Finance API（免费）
- 工作量：2天

**机器人公司追踪**
```
🤖 机器人追踪
├── Tesla Bot (Optimus) - 最新动态
├── 宇树科技 - Go2/H1进展
├── 智元机器人 - 融资/产品
└── Figure/1X - 海外竞品
```
- 实现：增加专题RSS源 + 话题聚合
- 工作量：1天

---

> 📋 完整设计文档见 [`docs/ROADMAP.md`](./docs/ROADMAP.md)

---

## 🚀 快速开始

### 方式一：云端部署（推荐）

1. Fork 本项目到你的 GitHub
2. 在 [Render](https://render.com) 创建账号
3. 参考 [`CLOUD_DEPLOY.md`](./CLOUD_DEPLOY.md) 配置
4. 连接 [MongoDB Atlas](https://www.mongodb.com/atlas)（免费版够用）

### 方式二：本地开发

```bash
# 1. 克隆项目
git clone https://github.com/Luffy-D-Monkey666/news-brief-platform.git
cd news-brief-platform

# 2. 启动依赖服务
docker run -d -p 27017:27017 --name mongo mongo:6
docker run -d -p 6379:6379 --name redis redis:7

# 3. 配置环境变量
cp ai-service/.env.example ai-service/.env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 4. 启动服务
cd ai-service && pip install -r requirements.txt && python src/main.py &
cd ../backend && npm install && npm run dev &
cd ../frontend && npm install && npm start
```

---

## 📡 API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/briefs/latest` | 获取最新简报 |
| GET | `/api/briefs/history` | 分页获取历史 |
| GET | `/api/briefs/stats` | 分类统计 |
| GET | `/api/topics/hot` | 获取热门话题 |
| GET | `/api/topics/:id` | 话题详情及相关新闻 |

---

## 🐛 常见问题

### AI Service 长时间没有新新闻
- Render 免费版 Worker 会休眠，访问前端会自动唤醒
- 检查 Render Dashboard → AI Service → Logs

### 简报只显示一句话
- 只有新抓取的新闻才会用新格式
- 旧数据需要等待新新闻自动进入

### 话题视图为空
- 话题需要同一事件≥2篇报道才会形成
- 新部署后需要等待数据积累

---

## 📁 项目结构

```
news-brief-platform/
├── ai-service/           # Python AI服务
│   ├── src/
│   │   ├── crawlers/     # RSS新闻爬虫
│   │   ├── processors/   # AI处理器
│   │   └── services/     # 话题聚合等服务
│   └── config/           # 新闻源、提示词配置
├── backend/              # Node.js 后端
│   └── src/
│       ├── routes/       # API路由（briefs, topics）
│       └── services/     # WebSocket服务
├── frontend/             # React 前端
│   └── src/
│       ├── components/   # BriefCard, TopicCard等
│       └── pages/        # HomePage
└── docs/                 # 文档
```

---

## 🤝 贡献指南

1. Fork 本项目
2. 创建功能分支：`git checkout -b feature/xxx`
3. 提交更改：`git commit -m "feat: 添加xxx功能"`
4. 推送并创建 Pull Request

---

## 📄 许可证

MIT License

---

**NewsHub** - 让新闻阅读更高效 📰
