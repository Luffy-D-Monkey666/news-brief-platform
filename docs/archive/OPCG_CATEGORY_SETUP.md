# OPCG卡牌游戏分类配置文档

**配置时间**: 2026-02-04
**分类名称**: OPCG卡牌游戏 (One Piece Card Game)
**英文ID**: `opcg_tcg`

---

## 🎮 分类概述

### 基本信息
- **英文ID**: `opcg_tcg`
- **中文名称**: `OPCG卡牌`
- **优先级**: 核心关注领域
- **图标**: FaGamepad（游戏手柄）🎮
- **颜色**: Orange（橙色，符合海贼王主题）
- **覆盖范围**: One Piece Card Game的所有相关内容

### 内容范围

**包含**:
- 官方公告和新闻（发售日期、禁限表、规则更新）
- 赛事资讯（锦标赛、旗舰赛、比赛结果）
- 卡片发售（新卡包、单卡卡面、异画编号卡）
- 价格行情（二级市场、单卡价格、投资收藏）
- 玩法攻略（Meta分析、卡组推荐、对局复盘）
- 社区动态（玩家讨论、开箱、抽卡）

**排除**:
- 单纯的海贼王动漫/漫画新闻（无卡牌元素）→ 归入 `entertainment_sports`

---

## 📊 关键词体系（80+关键词）

### 1. 游戏机制与环境（13个关键词）
```
卡组, deck, Meta, 环境, 上位卡组, top deck,
禁限表, Ban List, Restricted, Banned, Errata, 规则更新,
锦标赛, tournament, championship, 旗舰赛, 比赛, 赛事,
胜率, win rate, 对局, match, 复盘, deck building
```

**用途**: 捕获竞技环境、赛事信息、Meta分析

### 2. 卡片相关（18个关键词）
```
单卡, 卡面, card reveal, 新卡, 卡包, booster pack,
异画, alternate art, AA卡, 平行卡, parallel,
编号卡, 稀有度, rarity, SR, SEC, L卡, leader card,
角色卡, character card, 事件卡, event card,
场地卡, stage card, 船长卡, crew
```

**用途**: 捕获新卡发售、卡面公布、稀有卡片信息

### 3. 市场与价格（9个关键词）
```
价格, price, 行情, market, 交易, trade,
TCGPlayer, Cardmarket, Yu-Yu-Tei, 单卡价格,
投资, collection, 收藏, 保值, value
```

**用途**: 捕获二级市场价格波动、投资收藏信息

### 4. 官方与品牌（8个关键词）
```
万代, Bandai, 官方, official, 发售, release,
中文版, 日版, 英文版, 亚洲版,
onepiece-cardgame.com, onepiece-cardgame.cn
```

**用途**: 捕获官方公告、产品发售信息

### 5. 数据库与工具（6个关键词）
```
One Piece Top Decks, Ohara TCG, OP TCG Dex,
OneCollector, 卡组数据库, deck database
```

**用途**: 捕获技术流内容、数据分析

### 6. 玩家与社区（11个关键词）
```
Reddit OnePieceTCG, Wossy Plays, The Egman, VvTheory,
玩家, player, 玩法, strategy, 攻略, guide,
开箱, unboxing, 抽卡, pull, box break
```

**用途**: 捕获社区讨论、玩家体验、开箱视频

### 7. 海贼王角色（15个关键词）
```
路飞, Luffy, 索隆, Zoro, 娜美, Nami,
香吉士, Sanji, 乔巴, Chopper, 罗宾, Robin,
布鲁克, Brook, 佛朗基, Franky, 乌索普, Usopp,
艾斯, Ace, 白胡子, Whitebeard, 黑胡子, Blackbeard,
凯多, Kaido, 大妈, Big Mom, 红发, Shanks
```

**注意**: 角色关键词需要结合"卡牌"相关词汇才会匹配，避免误分类动漫新闻

---

## 📡 RSS信息源（4个核心源）

### 1. Reddit社区
```
URL: https://rsshub.app/reddit/r/OnePieceTCG
类型: 玩家讨论社区
内容: Meta分析、卡组分享、价格讨论、玩法交流
更新频率: 高
价值: ⭐⭐⭐⭐⭐
```

### 2. Wossy Plays (YouTube)
```
URL: https://rsshub.app/youtube/user/@WossyPlays
类型: 新闻博主
内容: 全球OPCG新闻整合、官方公告解读、新卡测评
更新频率: 极高（最勤快的OPCG博主）
价值: ⭐⭐⭐⭐⭐
```

### 3. The Egman (YouTube)
```
URL: https://rsshub.app/youtube/user/@TheEgman
类型: 赛事数据分析
内容: Meta报告、赛事统计、卡组胜率分析
更新频率: 中等
价值: ⭐⭐⭐⭐
```

### 4. VvTheory (YouTube)
```
URL: https://rsshub.app/youtube/user/@VvTheory
类型: 深度对局复盘
内容: 对局视频、新卡测评、卡组构筑指南
更新频率: 中等
价值: ⭐⭐⭐⭐
```

### 可选扩展源（未添加，可后续补充）

**官方新闻**:
- 中文官网: onepiece-cardgame.cn/news
- 日本官网: onepiece-cardgame.com/topics
- 英语官网: en.onepiece-cardgame.com/topics

**数据库与工具**:
- One Piece Top Decks: onepiecetopdecks.com（暂无RSS）
- Ohara TCG: oharatcg.com（暂无RSS）
- OP TCG Dex: optcgdex.com（暂无RSS）

**价格行情**:
- TCGPlayer: tcgplayer.com（暂无RSS）
- Cardmarket: cardmarket.com（暂无RSS）
- Yu-Yu-Tei: yuyu-tei.jp（暂无RSS）

---

## 🎯 分类判断规则

### 核心规则
```
必须同时满足两个条件：
1. 包含"海贼王/One Piece"相关词汇
2. 包含"卡牌/TCG/Card Game"相关词汇
```

### 判断示例

**✅ 归入 opcg_tcg**:
- "海贼王卡牌游戏新版本发售"（海贼王 + 卡牌）
- "One Piece TCG锦标赛结果公布"（One Piece + TCG）
- "路飞L卡单卡价格突破1000元"（路飞 + 卡 + 价格）
- "OPCG禁限表更新"（OPCG）
- "万代公布海贼王卡牌新卡包"（海贼王 + 卡牌 + 卡包）

**❌ 不归入 opcg_tcg**:
- "《海贼王》漫画最新话发布"（无卡牌元素）→ entertainment_sports
- "路飞声优访谈"（无卡牌元素）→ entertainment_sports
- "海贼王真人版Netflix"（无卡牌元素）→ entertainment_sports
- "游戏王卡牌价格上涨"（非海贼王）→ entertainment_sports 或 general

---

## 🔧 技术实现

### 修改的文件

#### 1. AI Service配置
[ai-service/config/settings.py](ai-service/config/settings.py)

```python
# Line 19: 添加到CATEGORIES
CATEGORIES = [
    'ai_technology',
    'robotics',
    'ai_programming',
    'opcg_tcg',  # 新增
    'ev_automotive',
    ...
]

# Line 39: 添加到CATEGORY_NAMES
CATEGORY_NAMES = {
    'ai_technology': 'AI技术',
    'robotics': '机器人',
    'ai_programming': 'AI编程',
    'opcg_tcg': 'OPCG卡牌',  # 新增
    ...
}

# Line 80-86: 添加RSS源
# ==================== OPCG卡牌游戏（4个核心源）====================
'https://rsshub.app/reddit/r/OnePieceTCG',
'https://rsshub.app/youtube/user/@WossyPlays',
'https://rsshub.app/youtube/user/@TheEgman',
'https://rsshub.app/youtube/user/@VvTheory',

# Line 380-426: 添加分类关键词和判断规则
4. opcg_tcg - OPCG卡牌游戏
   关键词：OPCG, One Piece Card Game, 海贼王卡牌...
   判断：所有与One Piece Card Game相关的内容...
```

#### 2. AI处理器
[ai-service/src/processors/cloud_ai_processor.py](ai-service/src/processors/cloud_ai_processor.py:223)

```python
# Line 223: 更新valid_categories
valid_categories = [
    'ai_technology', 'robotics', 'ai_programming', 'opcg_tcg',
    'ev_automotive', 'finance_investment',
    ...
]
```

#### 3. Backend数据库模型
[backend/src/models/Brief.js](backend/src/models/Brief.js:18)

```javascript
// Line 18: 更新category枚举
enum: [
  'ai_technology',
  'robotics',
  'ai_programming',
  'opcg_tcg',  // 新增
  'ev_automotive',
  ...
]
```

#### 4. Frontend分类过滤器
[frontend/src/components/CategoryFilter.js](frontend/src/components/CategoryFilter.js)

```javascript
// Line 17: 导入FaGamepad图标
import { ..., FaGamepad } from 'react-icons/fa';

// Line 24: 添加categoryIcons
const categoryIcons = {
  ai_technology: { icon: FaBrain, color: 'text-purple-600', ... },
  robotics: { icon: FaRobot, color: 'text-indigo-600', ... },
  ai_programming: { icon: FaCode, color: 'text-blue-600', ... },
  opcg_tcg: { icon: FaGamepad, color: 'text-orange-600', highlight: true, special: true },
  ...
};

// Line 42: 添加categoryNames
const categoryNames = {
  ai_technology: 'AI技术',
  robotics: '机器人',
  ai_programming: 'AI编程',
  opcg_tcg: 'OPCG卡牌',
  ...
};
```

#### 5. Frontend新闻卡片
[frontend/src/components/BriefCard.js](frontend/src/components/BriefCard.js)

```javascript
// Line 18: 添加categoryColors
const categoryColors = {
  ai_technology: 'text-purple-600',
  robotics: 'text-indigo-600',
  ai_programming: 'text-blue-600',
  opcg_tcg: 'text-orange-600',
  ...
};

// Line 33: 添加categoryNames
const categoryNames = {
  ai_technology: 'AI技术',
  robotics: '机器人',
  ai_programming: 'AI编程',
  opcg_tcg: 'OPCG卡牌',
  ...
};
```

---

## 🚀 部署与验证

### 自动部署
✅ 代码已推送到GitHub main分支
⏳ Render会自动检测更新并重新部署（5-10分钟）

### 部署验证步骤

**5-10分钟后检查**:

1. **访问Render Dashboard → AI Service → Logs**
2. 等待下一轮新闻抓取（最多5分钟）
3. 搜索日志关键词: `"opcg_tcg"` 或 `"OPCG"`
4. 验证新闻是否被正确分类到OPCG类别

**预期日志**:
```
处理完成: [opcg_tcg] One Piece TCG锦标赛结果...
处理完成: [opcg_tcg] 海贼王卡牌新版本发售...
处理完成: [opcg_tcg] 路飞L卡价格突破新高...
```

### 前端验证

**刷新网站后检查**:
1. 前端分类按钮应显示"OPCG卡牌"🎮图标
2. 点击"OPCG卡牌"分类，应该看到相关新闻
3. 新闻卡片分类标签应显示橙色的"OPCG卡牌"

---

## 📈 预期效果

### 新闻来源覆盖

| 来源类型 | 预期捕获率 | 主要渠道 |
|---------|-----------|---------|
| Reddit社区讨论 | 80%+ | r/OnePieceTCG |
| YouTube新闻 | 90%+ | Wossy Plays, The Egman, VvTheory |
| 官方公告 | 60%+ | 通过社区二次传播 |
| 价格行情 | 50%+ | 社区讨论中提及 |
| 赛事资讯 | 70%+ | YouTube赛事分析 |

### 分类准确率

- **目标准确率**: 85%+
- **主要挑战**: 区分海贼王动漫新闻和卡牌游戏新闻
- **解决方案**: 必须同时包含"海贼王"和"卡牌"关键词

### 内容丰富度

预计每天可捕获：
- **Reddit帖子**: 5-10篇（社区讨论、Meta分析）
- **YouTube视频**: 1-3个（新闻、测评、对局）
- **总计**: 6-13条OPCG相关新闻

---

## 🔄 后续优化建议

### 1. RSS源扩展

**优先级高**:
- X (Twitter) @ONEPIECE_tcg（日本官方推特）
- X (Twitter) @Official_OPCG（英文官方推特）

**优先级中**:
- 官方网站RSS（需要RSSHub自定义规则）
- 更多YouTube内容创作者

**优先级低**:
- 数据库网站（无RSS，需要爬虫）
- 价格行情网站（无RSS，需要爬虫）

### 2. 关键词微调

**观察期**: 部署后1-2天

**调整方向**:
- 如果误分类海贼王动漫新闻 → 增强"卡牌"相关词汇的权重
- 如果漏掉卡牌新闻 → 补充新的品牌、产品、术语
- 如果捕获率低 → 分析Reddit/YouTube内容，补充热门词汇

### 3. 与其他分类的边界

**需要注意的边界**:
- **opcg_tcg vs entertainment_sports**: 区分卡牌游戏和动漫本身
- **opcg_tcg vs general**: 确保OPCG相关词汇足够全面

---

## 📋 用户反馈收集

### 需要关注的指标
- [ ] OPCG分类是否有新闻出现？
- [ ] 新闻内容是否准确（无误分类）？
- [ ] 是否有漏掉的重要OPCG新闻？
- [ ] 新闻来源是否多样（Reddit + YouTube均有）？

### 反馈渠道
如果发现问题，请提供：
1. 具体的新闻标题和来源
2. 期望的分类 vs 实际分类
3. 建议补充的关键词或RSS源

---

**创建时间**: 2026-02-04
**Git Commit**: f598d6f
**状态**: ✅ 已部署，等待验证
**RSS源数**: 4个
**关键词数**: 80+
**预期每日新闻**: 6-13条
