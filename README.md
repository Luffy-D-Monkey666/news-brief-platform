# NewsHub - AI新闻聚合平台

一个基于AI的实时新闻聚合和简报系统，支持多分类新闻自动提炼、结构化展示和实时推送。

## 🌐 在线体验

- **前端**: https://news-frontend-e14o.onrender.com
- **API**: https://news-backend-rp9y.onrender.com

> ⚠️ 免费版 Render 会休眠，首次访问可能需要等待 30-50 秒唤醒

---

## ✨ 功能特性

### 核心功能
- ✅ **84+ 全球新闻源** - 覆盖AI、机器人、芯片、汽车、财经等18个分类
- ✅ **AI智能提炼** - DeepSeek驱动，自动生成结构化简报
- ✅ **三段式简报** - 事件概述 → 原文引用 → 重要细节 → 后续影响
- ✅ **实时推送** - WebSocket，无需刷新
- ✅ **时间筛选** - 1小时内/今日/本周
- ✅ **三种视图** - 卡片瀑布流/列表/话题聚合
- ✅ **语音朗读** - 浏览器原生TTS（火山引擎TTS开发中）

### v2.0 内容增强（2026-02-18）
- ✅ **原文关键引用** - 保留1-2句原文金句
- ✅ **来源可信度标识** - 🏛️官方/📰权威/🔬专业/💬社区 四级分类
- ✅ **Breaking News** - 重要新闻红色高亮+边框
- ✅ **行动建议** - 财经类新闻显示风险提示和行动建议
- ✅ **关键数字提取** - 自动提取营收/用户数等关键指标
- ✅ **背景知识+时间线** - 重要新闻显示背景介绍和事件发展历程
- ✅ **话题聚合** - 同一事件多篇报道自动归类，话题视图展示

### v2.1 深度内容增强（2026-02-18）
- ✅ **技术解读** - AI/芯片/机器人类新闻增加技术原理、对比、成熟度分析
- ✅ **融资历史** - 融资新闻显示该公司历史融资记录和估值
- ✅ **供应链视角** - 消费电子/汽车类新闻分析关联供应商和产能信息
- ✅ **股票数据** - 上市公司新闻自动补充市值、PE、涨跌幅（计划接入Yahoo Finance）

### v2.2 音频播放功能（2026-02-19）
- ✅ **音频播放器** - 底部固定播放控制栏
- ✅ **连续播放** - 自动播放下一条新闻
- ✅ **播放控制** - 播放/暂停、上一条/下一条
- ✅ **音频视图** - 简化卡片模式，专注听新闻
- ⏳ **云端TTS** - 火山引擎豆包语音合成（开发中）

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
│    Tailwind CSS + Socket.io + Masonry + AudioPlayer         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (Node.js)                          │
│       Express + MongoDB + Redis + Socket.io + TTS API       │
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
| TTS | 火山引擎豆包语音合成（开发中） |
| 部署 | Docker, Render |

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

📈 股票信息（上市公司新闻）
   TSLA $248.50 +2.3% | 市值 8000亿 | PE 65

📚 背景知识（重要新闻）
   公司/人物背景 + 事件时间线

🔬 技术解读（AI/芯片/机器人类）
   技术原理 + 对比 + 成熟度

💰 融资历史（融资新闻）
   历史融资轮次 + 投资方 + 估值

🔗 供应链视角（消费电子/汽车类）
   影响分析 + 关联公司 + 产能信息

⚠️ 行动建议（财经类）
   风险提示 + 操作建议
```

---

## 🗺️ 开发路线图

### ✅ 已完成

| 版本 | 功能 | 完成日期 |
|------|------|----------|
| v1.0 | 基础新闻聚合、三段式简报、实时推送 | 2026-02-17 |
| v2.0 | 原文引用、可信度标识、Breaking News、话题聚合 | 2026-02-18 |
| v2.1 | 技术解读、融资历史、供应链视角、关键数字提取 | 2026-02-18 |
| v2.2 | 音频播放器、连续播放、音频视图 | 2026-02-19 |

### 🔜 开发中

| 功能 | 说明 | 状态 |
|------|------|------|
| **火山引擎TTS** | 接入豆包语音合成，替代浏览器原生TTS | 🔧 调试中 |
| **Yahoo Finance** | 实时股票数据接入 | ⏳ 待开发 |

### 📋 待规划

| 优先级 | 功能 | 说明 |
|--------|------|------|
| 🥇 | 语音早报 | 每日自动生成5分钟语音版新闻摘要 |
| 🥇 | 机器人公司追踪 | Tesla Bot/宇树/智元等重点公司动态聚合 |
| 🥈 | 个性化首页 | 根据用户关注领域生成「我的日报」 |
| 🥈 | 一键分享 | 生成精美的分享卡片 |
| 🥉 | OPCG独立分类 | 海贼王卡牌从TCG中独立 |

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
| GET | `/api/tts/voices` | 获取可用音色列表 |
| POST | `/api/tts/synthesize` | 文本转语音 |

---

## 📁 项目结构

```
news-brief-platform/
├── ai-service/      # Python AI服务 (爬虫+处理)
├── backend/         # Node.js 后端 (API+WebSocket)
├── frontend/        # React 前端
└── docs/            # 详细文档
```

详细结构见各子目录 README。

---

## 🔄 自动运行机制

系统部署后**完全自动运行**，无需人工干预：

| 组件 | 行为 | 间隔 |
|------|------|------|
| AI Service | 自动采集 RSS → AI 处理 → 存入数据库 | 每 5 分钟 |
| UptimeRobot | 防止 Render 免费版休眠 | 每 5 分钟 |
| Frontend/Backend | 按需响应用户请求 | - |

### 🛡️ 保活配置 (UptimeRobot)

Render 免费版会在无流量时休眠。使用 [UptimeRobot](https://uptimerobot.com)（免费）防止休眠：

1. 注册 UptimeRobot 账号
2. 添加 HTTP(s) Monitor：
   - **URL**: `https://news-platform-ai-service.onrender.com`
   - **Interval**: 5 minutes
3. 完成！AI Service 将保持 24/7 运行

### ✅ 你只需关注

- **DeepSeek API 余额** - 确保有足够余额（约 ¥10/月）
- 其他一切自动运行

---

## 💰 运营成本

| 项目 | 月费用 | 说明 |
|------|--------|------|
| DeepSeek API | ~¥10 | 新闻处理，约 2300 tokens/条 |
| Render | $0 | 免费版 + UptimeRobot 保活 |
| MongoDB Atlas | $0 | 免费版 512MB |
| UptimeRobot | $0 | 免费版 50 monitors |
| **合计** | **~¥10/月** | |

---

## 📚 更多文档

- [FAQ - 常见问题](./docs/FAQ.md)
- [部署指南](./docs/DEPLOYMENT_STEPS.md)
- [开发路线图](./docs/ROADMAP.md)
- [归档文档](./docs/archive/) - 开发过程记录

---

## 📄 许可证

MIT License

---

**NewsHub** - 让新闻阅读更高效 📰
