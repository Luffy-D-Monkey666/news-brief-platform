# NewsHub - AI新闻聚合平台

一个基于AI的实时新闻聚合和简报系统，支持多分类新闻自动提炼、结构化展示、语音播报和实时推送。

## 🌐 在线体验

- **前端**: https://news-frontend-e14o.onrender.com
- **API**: https://news-backend-rp9y.onrender.com

> ⚠️ 免费版 Render 会休眠，首次访问可能需要等待 30-50 秒唤醒

---

## ✨ 功能特性

- ✅ **84+ 全球新闻源** - 覆盖AI、机器人、芯片、汽车、财经等18个分类
- ✅ **AI智能提炼** - DeepSeek驱动，自动生成结构化三段式简报
- ✅ **实时推送** - WebSocket，无需刷新
- ✅ **时间筛选** - 1小时内/今日/本周
- ✅ **四种视图** - 卡片瀑布流/列表/话题聚合/音频
- ✅ **语音朗读** - 火山引擎豆包 TTS，30+ 高质量音色
- ✅ **话题聚合** - 同一事件多篇报道自动归类
- ✅ **来源可信度** - 🏛️官方/📰权威/🔬专业/💬社区 四级分类

---

## 🚀 快速开始

### 方式一：云端部署（推荐）

1. Fork 本项目到你的 GitHub
2. 在 [Render](https://render.com) 创建账号
3. 参考 [部署文档](./docs/DEPLOYMENT_STEPS.md) 配置
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
# 编辑 .env 文件填写实际值

# 4. 启动服务
cd ai-service && pip install -r requirements.txt && python src/main.py &
cd ../backend && npm install && npm run dev &
cd ../frontend && npm install && npm start
```

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│         Tailwind CSS + Socket.io + AudioPlayer              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (Node.js)                          │
│          Express + MongoDB + Redis + Socket.io              │
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
| 前端 | React 18, Tailwind CSS, Socket.io-client |
| 后端 | Node.js 18+, Express, MongoDB, Redis |
| AI服务 | Python 3.9+, DeepSeek API |
| TTS | 火山引擎豆包语音合成 |
| 部署 | Render |

---

## 📁 项目结构

```
news-brief-platform/
├── frontend/        # React 前端
├── backend/         # Node.js 后端
├── ai-service/      # Python AI服务
├── shared/          # 共享配置
└── docs/            # 详细文档
```

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [API 文档](./docs/API.md) | 接口说明 |
| [部署指南](./docs/DEPLOYMENT_STEPS.md) | 云端部署步骤 |
| [TTS 配置](./docs/TTS_SETUP.md) | 火山引擎语音合成配置 |
| [FAQ](./docs/FAQ.md) | 常见问题 |
| [开发路线图](./docs/ROADMAP.md) | 功能规划 |

---

## 💰 运营成本

| 项目 | 月费用 | 说明 |
|------|--------|------|
| DeepSeek API | ~¥10 | 新闻处理 |
| 火山引擎 TTS | ~¥5-20 | 语音合成 |
| Render | $0 | 免费版 |
| MongoDB Atlas | $0 | 免费版 512MB |
| **合计** | **~¥15-30/月** | |

---

## 📄 许可证

[MIT License](./LICENSE)

---

**NewsHub** - 让新闻阅读更高效 📰
