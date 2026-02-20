# 热门实体预置开发计划

> 创建时间: 2026-02-20
> 状态: 待实施

---

## 目标

在现有知识库架构基础上，预置一批热门实体（公司、人物、概念等），使系统上线即可展示这些实体的时间轴页面。

---

## 现有架构分析

### 已完成的部分

1. **数据模型**
   - `Entity` 模型 (`backend/src/models/Entity.js`)
     - 支持 name, aliases, type, description, base_timeline
     - `is_preset` 字段标记预置实体
   - `EntityNews` 模型 - 实体与新闻的关联

2. **后端 API** (`backend/src/routes/entities.js`)
   - `POST /api/entities` - 创建实体（支持 is_preset）
   - `POST /api/entities/mention` - 记录提及
   - `POST /api/entities/:id/activate` - 激活实体
   - `GET /api/entities/:id/timeline` - 获取时间轴

3. **AI 实体服务** (`ai-service/src/services/entity_service.py`)
   - 自动识别新闻中的实体
   - 阈值机制（mention_count 达到阈值后激活）
   - AI 生成基础时间轴

### 缺少的部分

1. **预置数据脚本** - 没有批量导入预置实体的工具
2. **热门实体数据** - 没有准备好的实体清单和时间轴

---

## 实体清单设计

### 分类维度

| 类型 | 说明 | 示例 |
|------|------|------|
| company | 科技/汽车/金融公司 | 特斯拉, OpenAI, 苹果 |
| person | 商界/科技界人物 | 马斯克, Sam Altman |
| concept | 技术/行业概念 | GPT, 大模型, AGI |
| event | 持续性重大事件 | 俄乌战争, 中美关系 |

### 初步热门实体清单 (50+)

#### 科技公司 (15)
1. **特斯拉** (Tesla) - 电动汽车、能源
2. **OpenAI** - AI 研究
3. **苹果** (Apple) - 消费电子、AI
4. **英伟达** (NVIDIA) - GPU、AI芯片
5. **谷歌** (Google/Alphabet) - AI、搜索
6. **微软** (Microsoft) - AI、云计算
7. **亚马逊** (Amazon) - 电商、云
8. **Meta** - 社交、AI
9. **字节跳动** (ByteDance) - 短视频、AI
10. **腾讯** (Tencent) - 游戏、社交
11. **阿里巴巴** (Alibaba) - 电商、云
12. **百度** (Baidu) - AI、搜索
13. **华为** (Huawei) - 通信、芯片
14. **小米** (Xiaomi) - 手机、IoT
15. **比亚迪** (BYD) - 电动汽车、电池

#### AI 公司/实验室 (10)
1. **Anthropic** - Claude
2. **DeepMind** - AI 研究
3. **xAI** - Grok
4. **Mistral AI** - 开源大模型
5. **智谱AI** (Zhipu) - GLM
6. **月之暗面** (Moonshot) - Kimi
7. **MiniMax** - AI
8. **零一万物** (01.AI) - Yi
9. **深势科技** (DeepSeek) - DeepSeek
10. **Stability AI** - Stable Diffusion

#### 芯片/硬件 (5)
1. **AMD** - GPU、CPU
2. **英特尔** (Intel) - CPU
3. **台积电** (TSMC) - 芯片代工
4. **高通** (Qualcomm) - 手机芯片
5. **ARM** - 芯片架构

#### 人物 (10)
1. **马斯克** (Elon Musk) - Tesla/SpaceX/xAI
2. **Sam Altman** - OpenAI
3. **黄仁勋** (Jensen Huang) - NVIDIA
4. **蒂姆·库克** (Tim Cook) - Apple
5. **萨蒂亚·纳德拉** (Satya Nadella) - Microsoft
6. **马克·扎克伯格** (Mark Zuckerberg) - Meta
7. **李彦宏** - 百度
8. **雷军** - 小米
9. **王传福** - 比亚迪
10. **Dario Amodei** - Anthropic

#### 技术概念 (8)
1. **GPT** - 大语言模型
2. **大模型** (LLM) - 语言模型
3. **AGI** - 通用人工智能
4. **Transformer** - 模型架构
5. **FSD** (Full Self-Driving) - 自动驾驶
6. **量子计算** - 新计算范式
7. **芯片制程** - 半导体工艺
8. **智能体** (AI Agent) - AI 应用

#### 重大事件 (5)
1. **中美贸易** - 贸易关系
2. **俄乌冲突** - 地缘政治
3. **巴以冲突** - 地缘政治
4. **加密货币监管** - 金融
5. **AI 监管** - 政策

---

## 开发任务

### 任务 1: 创建预置数据脚本

**文件**: `scripts/seed_entities.js`

**功能**:
- 读取 JSON 格式的实体清单
- 批量创建 Entity 记录
- 支持 upsert（存在则更新）
- 标记 `is_preset: true`

**执行方式**:
```bash
node scripts/seed_entities.js
# 或
node scripts/seed_entities.js --file entities/tech_companies.json
```

### 任务 2: 准备实体数据文件

**目录**: `data/entities/`

**文件结构**:
```
data/
└── entities/
    ├── tech_companies.json    # 科技公司
    ├── ai_companies.json      # AI 公司
    ├── chip_companies.json    # 芯片公司
    ├── persons.json           # 人物
    ├── concepts.json          # 技术概念
    └── events.json            # 重大事件
```

**单个实体格式**:
```json
{
  "name": "特斯拉",
  "aliases": ["Tesla", "TSLA"],
  "type": "company",
  "description": "美国电动汽车和清洁能源公司，由马斯克等人于2003年创立，引领全球电动汽车革命。",
  "metadata": {
    "founded": "2003",
    "founder": "埃隆·马斯克、JB·施特劳贝尔等",
    "headquarters": "美国德克萨斯州奥斯汀",
    "industry": "电动汽车、能源存储、太阳能",
    "ticker": "TSLA"
  },
  "base_timeline": [
    { "date": "2003.07", "event": "公司成立", "importance": "milestone" },
    { "date": "2008.02", "event": "首款电动跑车 Roadster 发布", "importance": "milestone" },
    { "date": "2010.06", "event": "IPO 上市，股价 $17", "importance": "milestone" },
    { "date": "2012.06", "event": "Model S 发布，开创豪华电动轿车市场", "importance": "major" },
    { "date": "2015.09", "event": "Model X SUV 发布", "importance": "major" },
    { "date": "2017.07", "event": "Model 3 量产，进入大众市场", "importance": "milestone" },
    { "date": "2019.03", "event": "Model Y 发布", "importance": "major" },
    { "date": "2020.01", "event": "市值超越丰田，成为全球最大车企", "importance": "milestone" },
    { "date": "2020.11", "event": "加入标普500指数", "importance": "major" },
    { "date": "2021.10", "event": "市值突破1万亿美元", "importance": "milestone" },
    { "date": "2022.12", "event": "Cybertruck 开始交付", "importance": "major" },
    { "date": "2024.10", "event": "Robotaxi 和 Optimus 机器人发布会", "importance": "major" }
  ]
}
```

### 任务 3: 实体数据整理

为 50+ 实体准备完整数据：
- 基本信息（名称、别名、描述）
- 元数据（成立时间、创始人等）
- 基础时间轴（5-15 个关键节点）

**优先级**:
1. 高频实体（特斯拉、OpenAI、苹果、英伟达、马斯克） - 详细时间轴
2. 中频实体 - 基础时间轴
3. 低频实体 - 仅基本信息

---

## 时间估算

| 任务 | 预计时间 |
|------|---------|
| 创建 seed 脚本 | 0.5h |
| 整理科技公司数据 (15个) | 1.5h |
| 整理 AI 公司数据 (10个) | 1h |
| 整理芯片公司数据 (5个) | 0.5h |
| 整理人物数据 (10个) | 1h |
| 整理概念/事件数据 (13个) | 1h |
| 测试 & 调试 | 0.5h |
| **总计** | **~6h** |

---

## 后续可扩展

1. **AI 辅助生成** - 用 AI 批量生成时间轴初稿，人工审核
2. **动态更新** - 定期更新预置实体的重大事件
3. **用户贡献** - 允许用户提交实体修正

---

## 开始条件

- [x] Entity 模型已支持 base_timeline
- [x] 后端 API 已支持创建预置实体
- [x] 知识库设计文档已完成

## 验收标准

- [ ] 50+ 预置实体入库
- [ ] 每个实体有 5+ 基础时间轴节点
- [ ] 前端知识库页面可正常展示
- [ ] 新闻自动关联到预置实体
