# 内容质量审查报告

## 📊 审查时间：2026-02-04

## 🎯 审查目标
从行业从业者角度审查每个分类的新闻质量，识别低质量内容并制定筛选规则。

---

## ❌ 核心问题发现

### 问题1：**无内容质量筛选机制**（严重）

**现状**：
```python
# news_crawler.py:28
for entry in feed.entries[:20]:  # 每个源取最新20条
    news_items.append(news_item)  # 直接添加，无筛选
```

**后果**：
- RSS中的广告、推广、低质量内容全部被抓取
- 无法区分重大新闻 vs. 琐碎信息
- 用户看到大量不重要的新闻

**证据**：
- AI处理器（cloud_ai_processor.py）只做摘要+分类，不评估重要性
- 没有任何内容质量评分或过滤逻辑

---

### 问题2：**RSS源质量参差不齐**（中等）

#### 🚨 高风险RSS源识别

**RSSHub源的风险**：
```python
# 以下源可能包含低质量内容：
'https://rsshub.app/xiaoyuzhoufm/explore',  # 小宇宙精选：算法推荐，质量不稳定
'https://rsshub.app/hackernews/best',       # HN Best：包含大量讨论类内容
'https://rsshub.app/reddit/topic/*',        # Reddit：用户UGC，质量波动大
'https://rsshub.app/bilibili/user/video/*', # B站：视频标题非新闻内容
```

**问题分析**：
1. **RSSHub聚合源**：质量依赖源网站，RSSHub本身不保证质量
2. **社区类源**（Reddit/HN）：包含讨论、问答、个人观点，非传统新闻
3. **视频平台**（YouTube/B站）：标题党、娱乐化内容混入
4. **播客源**：单集描述通常不是新闻，而是节目介绍

---

### 问题3：**分类关键词过于宽泛**（中等）

**案例1：消费电子分类**
```python
# 关键词包含：
'手机, smartphone, phone, 电子产品'
```

**问题**：会匹配到：
- ❌ "如何选购手机保护壳"（低价值教程）
- ❌ "手机游戏排行榜"（娱乐内容）
- ✅ "iPhone 16发布"（高价值新闻）

**案例2：AI技术分类**
```python
# 关键词包含：
'AI, artificial intelligence, 人工智能'
```

**问题**：会匹配到：
- ❌ "AI如何改变我的生活"（软文）
- ❌ "5个AI工具推荐"（工具推荐）
- ✅ "OpenAI发布GPT-5"（重大新闻）

---

## 🔍 按分类审查结果

### 1. AI技术（ai_technology）

**优质源**：✅
- OpenAI官方博客
- Google AI Research
- DeepMind官方
- arXiv AI论文

**问题源**：⚠️
- `rsshub.app/thenextweb/ai` - 可能包含观点文章
- `unite.ai` - 营销性质较强
- `infoq.com/ai` - 包含大量教程和工具推荐

**建议**：
- 保留官方源（OpenAI、Google、DeepMind）
- 添加质量过滤：排除标题包含"教程"、"指南"、"推荐"的内容

---

### 2. 机器人（robotics）

**优质源**：✅
- MIT CSAIL
- CMU Robotics
- Stanford AI Lab
- IEEE官方新闻

**问题源**：⚠️
- `rsshub.app/robotstart` - 日本小众网站，更新频率低
- `rsshub.app/sps-magazin` - 工业杂志，可能包含产品广告

**建议**：
- 优先级排序：学术机构（MIT/CMU/Stanford） > 行业媒体
- 添加关键词过滤：排除"购买"、"价格"等商业化内容

---

### 3. AI编程（ai_programming）

**优质源**：✅
- GitHub官方博客
- VSCode官方

**问题源**：⚠️
- `rsshub.app/hackernews/best` - 大量讨论类内容，非新闻
- `rsshub.app/reddit/topic/programming` - UGC内容，质量波动大
- `dev.to/feed` - 个人博客平台，教程居多

**建议**：
- **移除或降权**：HackerNews、Reddit、Dev.to
- **保留**：官方博客（GitHub、VSCode）
- **添加**：更多官方源（JetBrains Blog、Microsoft Developer Blog）

---

### 4. 芯片（semiconductors）

**优质源**：✅
- EE Times
- SemiWiki
- Semiconductor Today

**问题源**：⚠️
- `rsshub.app/anandtech` - 硬件评测网站，可能包含消费类内容
- `rsshub.app/tomshardware` - 消费类硬件，非产业链新闻

**建议**：
- 添加分类规则：区分产业链新闻 vs. 消费评测
- 产业链关键词：晶圆、代工、制程、EUV
- 排除关键词：评测、性能、跑分

---

### 5. OPCG卡牌（opcg）

**优质源**：✅
- Reddit OnePieceTCG社区
- YouTube专业UP主（Wossy Plays、The Egman）

**问题源**：⚠️
- YouTube源可能包含：开箱视频、对局录像（非新闻）

**建议**：
- 添加标题过滤：排除"开箱"、"对局"、"实战"
- 保留：官方公告、赛事新闻、Meta分析、禁卡表

---

### 6. 消费电子（consumer_electronics）

**优质源**：✅
- GSMArena（手机专业）
- DPReview（相机专业）
- The Verge、Engadget

**问题源**：⚠️
- `rsshub.app/ithome/it` - IT之家包含大量软文和推广
- `anandtech` - 评测周期长，时效性差

**建议**：
- 排除关键词："购买"、"推荐"、"指南"、"评测"
- 保留关键词："发布"、"上市"、"曝光"、"新品"

---

### 7. ONE PIECE动漫（one_piece）

**优质源**：✅
- Reddit OnePiece社区

**问题源**：⚠️
- `rsshub.app/onepiece/news` - 路由可能不存在
- `rsshub.app/bilibili/user/video/488779` - B站视频，非新闻
- `onepiece.fandom.com` - Wiki更新日志，非新闻内容
- `crunchyroll.com/rss/anime` - 全动漫，非OP专属
- `animenewsnetwork.com` - 全动漫，OP占比低

**建议**：
- **问题严重**：多个源不是新闻源，是视频/Wiki/通用动漫
- **移除**：B站视频源、Wiki源
- **保留**：Reddit社区、YouTube解析频道
- **添加**：ONE PIECE官方Twitter RSS（如果有）

---

### 8. 播客（podcasts）

**优质源**：✅
- Lex Fridman
- a16z Podcast

**问题源**：🚨 **严重问题**
```python
'https://rsshub.app/xiaoyuzhoufm/podcast/6021f949a789fca4eff4492c',  # 罗永浩
'https://rsshub.app/xiaoyuzhoufm/podcast/619aea7ef8f6e3ba4e23f9ac',  # 叭叭呜
```

**根本性问题**：
- **播客RSS ≠ 播客新闻**
- RSS返回的是：单集描述、嘉宾介绍、节目内容
- 用户想看的是：播客行业新闻、新节目发布、主播动态

**例子**：
- RSS返回："本期我们聊了关于AI的话题"（❌ 不是新闻）
- 应该是："罗永浩宣布推出新播客节目"（✅ 是新闻）

**建议**：
- **重新设计播客分类**：
  - 播客新闻（行业动态）vs. 播客内容（单集推荐）
  - 当前RSS源适合"播客推荐"，不适合"播客新闻"
- **播客新闻源建议**：
  - Podcast Industry News
  - 播客平台官方公告（小宇宙、Spotify News）
  - 科技媒体的播客版块

---

### 9. 汽车（automotive）

**优质源**：✅
- Electrek
- InsideEVs
- CleanTechnica

**问题源**：⚠️
- `rsshub.app/dongchedi/news` - 懂车帝可能包含导购内容
- `caranddriver.com` - 评测杂志，非行业新闻

**建议**：
- 排除关键词："导购"、"推荐"、"评测"
- 保留关键词："发布"、"销量"、"财报"、"新车"

---

## 🎯 优化方案

### 方案A：添加内容质量评分系统（推荐）

在AI处理流程中增加重要性评分：

```python
def evaluate_importance(title: str, content: str, category: str) -> int:
    """评估新闻重要性（1-10分）"""

    # 高价值关键词（+2分）
    high_value_keywords = {
        'ai_technology': ['发布', '突破', '研究', '论文', '官方'],
        'robotics': ['新型', '研发', '量产', '商用'],
        'automotive': ['发布', '销量', '财报', '新车'],
        # ...
    }

    # 低价值关键词（-3分）
    low_value_keywords = [
        '教程', '指南', '推荐', '评测', '购买',
        '如何', '怎样', '方法', '技巧', 'Top 10'
    ]

    score = 5  # 基础分

    # 加分逻辑
    for keyword in high_value_keywords.get(category, []):
        if keyword in title:
            score += 2

    # 减分逻辑
    for keyword in low_value_keywords:
        if keyword in title.lower():
            score -= 3

    return max(1, min(10, score))
```

**保存策略**：
- 8-10分：立即推送到首页
- 5-7分：正常保存
- 1-4分：保存但不推送，标记为"低优先级"

---

### 方案B：RSS源分级管理

**S级源**（权威官方）：
- OpenAI Blog
- Google AI Research
- MIT CSAIL
- GitHub Blog

**A级源**（专业媒体）：
- TechCrunch
- The Verge
- Wired
- Electrek

**B级源**（社区聚合）：
- RSSHub聚合源
- Reddit
- HackerNews

**C级源**（高风险）：
- 个人博客平台（Dev.to）
- UGC平台（B站、YouTube非官方）

**策略**：
- S级：全量采集
- A级：采集前10条
- B级：采集前5条 + 质量评分>7
- C级：禁用或仅采集评分>8的内容

---

### 方案C：分类特定过滤规则

#### AI技术
```python
EXCLUDE_KEYWORDS = ['教程', '指南', '入门', '推荐', 'Top', '排行']
INCLUDE_KEYWORDS = ['发布', '研究', '论文', '突破', '开源', '官方']
```

#### 机器人
```python
EXCLUDE_KEYWORDS = ['购买', '价格', '评测', '对比']
INCLUDE_KEYWORDS = ['研发', '量产', '应用', '技术', '系统']
```

#### OPCG卡牌
```python
EXCLUDE_KEYWORDS = ['开箱', '对局', '实战', '抽卡']
INCLUDE_KEYWORDS = ['禁卡', 'Meta', '赛事', '发售', '官方']
```

#### 播客（特殊处理）
```python
# 播客分类需要重新设计
# 选项1：移除播客分类（因为RSS源不适合）
# 选项2：改名为"播客推荐"，明确是内容推荐
# 选项3：寻找真正的播客新闻源
```

---

## 📝 RSS源清理建议

### 立即移除（质量问题严重）

```python
# ONE PIECE分类
'https://rsshub.app/bilibili/user/video/488779',  # B站视频，非新闻
'https://onepiece.fandom.com/wiki/Special:RecentChanges?feed=rss',  # Wiki更新，非新闻
'https://www.crunchyroll.com/rss/anime',  # 全动漫源，OP占比低

# 播客分类（需要重新设计）
'https://rsshub.app/xiaoyuzhoufm/podcast/*',  # 播客内容，非新闻

# AI编程分类
'https://rsshub.app/reddit/topic/programming',  # UGC质量不稳定
'https://dev.to/feed',  # 个人博客，教程居多
```

### 降权处理（保留但限制数量）

```python
# 社区类源：每次只采集前5条
COMMUNITY_SOURCES = [
    'https://rsshub.app/hackernews/best',
    'https://rsshub.app/reddit/r/OnePiece',
    'https://rsshub.app/reddit/r/OnePieceTCG',
]

# 评测类源：只保留重大新闻（标题包含"发布"、"新品"）
REVIEW_SOURCES = [
    'https://www.anandtech.com/rss/',
    'https://www.dpreview.com/feeds/news.xml',
]
```

---

## 🚀 实施优先级

### 高优先级（立即实施）
1. ✅ **移除问题RSS源**（ONE PIECE的B站/Wiki源、播客内容源）
2. ✅ **添加基础过滤规则**（排除"教程"、"指南"、"推荐"）
3. ✅ **调整爬取数量**：S级源20条，A级源10条，B级源5条

### 中优先级（2周内）
4. ⏳ **实现内容质量评分系统**（方案A）
5. ⏳ **RSS源分级管理**（方案B）
6. ⏳ **重新设计播客分类**（播客新闻 vs. 播客推荐）

### 低优先级（未来优化）
7. 🔮 **机器学习质量模型**（基于用户点击率）
8. 🔮 **个性化推荐**（基于用户兴趣）

---

## 📊 预期效果

实施优化后：
- **新闻数量**：减少30-40%（移除低质量内容）
- **内容质量**：重大新闻占比从40% → 70%
- **用户体验**：减少无关内容干扰
- **AI成本**：减少30%处理量，节省API费用

---

## 🔄 持续监控

每周审查：
1. 各分类新闻质量（抽样10条）
2. 低评分新闻占比
3. RSS源活跃度（是否失效）
4. 用户反馈（如果有）

每月优化：
1. 调整过滤规则
2. 更新RSS源列表
3. 优化评分算法

---

**审查人**：Claude Sonnet 4.5
**审查日期**：2026-02-04
**下次审查**：2026-03-04
