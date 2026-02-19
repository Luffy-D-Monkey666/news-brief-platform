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
- ✅ **火山引擎 TTS** - 豆包语音合成，30+ 高质量音色

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
| TTS | 火山引擎豆包语音合成 (30+ 音色) |
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
| 火山引擎 TTS | ~¥5-20 | 按字符计费，约 0.2元/万字符 |
| Render | $0 | 免费版 + UptimeRobot 保活 |
| MongoDB Atlas | $0 | 免费版 512MB |
| UptimeRobot | $0 | 免费版 50 monitors |
| **合计** | **~¥15-30/月** | |

---

## 🎤 火山引擎 TTS 部署指南

本项目使用**火山引擎豆包语音合成**提供高质量中文 TTS 服务，支持 30+ 音色。

### Step 1: 注册火山引擎账号

1. 打开 https://www.volcengine.com/
2. 点击右上角 **「注册」**
3. 支持手机号/邮箱注册，完成实名认证（需要身份证）

### Step 2: 开通语音合成服务

1. 登录后进入控制台：https://console.volcengine.com/
2. 在顶部搜索框搜索 **「语音技术」**，或直接访问：
   - https://console.volcengine.com/speech/app
3. 首次进入会提示 **「开通服务」**，点击开通（免费）
4. 阅读并同意服务协议

### Step 3: 购买资源包（可选但推荐）

> ⚠️ 不购买也可以使用，会按量后付费。购买资源包更便宜。

1. 进入 https://console.volcengine.com/speech/usage
2. 点击 **「购买资源包」**
3. 选择 **「语音合成」** 类型
4. 推荐购买：
   - **通用语音合成 - 100万字符包** ≈ ¥20（够用很久）
   - 或先用免费额度试用

### Step 4: 创建应用并获取凭证

1. 进入应用管理页面：https://console.volcengine.com/speech/app
2. 点击 **「创建应用」** 按钮
3. 填写信息：
   - **应用名称**: 如 `NewsHub-TTS`
   - **应用描述**: 如 `新闻语音播报`
   - **使用场景**: 选择 `语音合成`
4. 创建成功后，在应用列表点击应用名称进入详情
5. 记录以下信息：
   - **App ID**: 页面顶部显示，如 `6922135515`
6. 点击 **「生成 Token」** 按钮，复制生成的 **Access Token**

### Step 5: 配置环境变量

在 Backend 服务的环境变量中添加：

```bash
# 火山引擎 TTS 配置（必填）
VOLC_APP_ID=你的AppID（如 6922135515）
VOLC_ACCESS_TOKEN=你的AccessToken（很长的字符串）

# 可选配置（有默认值）
VOLC_CLUSTER=volcano_tts
```

**Render 部署配置方法**：
1. 打开 https://dashboard.render.com/
2. 点击你的 **Backend Service**（如 `news-backend`）
3. 左侧菜单选择 **「Environment」**
4. 在 **「Environment Variables」** 区域点击 **「Add Environment Variable」**
5. 分别添加 `VOLC_APP_ID` 和 `VOLC_ACCESS_TOKEN`
6. 点击 **「Save Changes」**，服务会自动重新部署

### Step 6: 验证配置

部署完成后，访问以下 URL 测试：

```
https://你的backend域名/api/tts/voices
```

如果返回音色列表 JSON，说明配置成功！

### 可用音色（30+）

| 分类 | 音色 | Voice ID |
|------|------|----------|
| **通用场景** | 灿灿 2.0 ⭐ | `BV700_V2_streaming` |
| | 炀炀 | `BV705_streaming` |
| | 擎苍 2.0 | `BV701_V2_streaming` |
| | 通用女声 | `BV001_streaming` |
| | 通用男声 | `BV002_streaming` |
| **超自然音色** | 梓梓 2.0 | `BV406_V2_streaming` |
| | 燃燃 2.0 | `BV407_V2_streaming` |
| **有声阅读** | 擎苍 | `BV701_streaming` |
| | 阳光青年 | `BV123_streaming` |
| | 古风少御 | `BV115_streaming` |
| | 儒雅青年 | `BV102_streaming` |
| | 温柔淑女 | `BV104_streaming` |
| **智能助手** | 甜美小源 | `BV405_streaming` |
| | 亲切女声 | `BV007_streaming` |
| | 知性女声 | `BV009_streaming` |
| **新闻播报** | 新闻女声 | `BV011_streaming` |
| | 新闻男声 | `BV012_streaming` |
| **视频配音** | 影视解说小帅 | `BV411_streaming` |
| | 影视解说小美 | `BV412_streaming` |
| **特色音色** | 奶气萌娃 | `BV051_streaming` |
| | 天才童声 | `BV061_streaming` |
| **英文** | Jackson (美式男) | `BV504_streaming` |
| | Ariana (美式女) | `BV503_streaming` |

### API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/tts/voices` | GET | 获取可用音色列表 |
| `/api/tts/synthesize` | POST | 合成语音 (body: `{text, voice?}`) |
| `/api/tts/brief/:id` | GET | 获取指定新闻的语音 (query: `?voice=xxx`) |

### 计费说明

- **计费单位**: 按字符数计费
- **价格**: 约 0.2 元 / 万字符（具体以官网为准）
- **免费额度**: 新用户有一定免费额度
- **缓存机制**: 系统内置 30 分钟音频缓存，减少重复调用

### 常见问题

**Q: 提示 "未配置 Access Token"？**
A: 检查环境变量 `VOLC_ACCESS_TOKEN` 是否正确设置。

**Q: 提示 "错误码 xxxx"？**
A: 参考[火山引擎错误码文档](https://www.volcengine.com/docs/6561/79820)排查。

**Q: 音频播放卡顿？**
A: 首次合成需要 1-2 秒，后续会命中缓存。检查网络状况。

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
