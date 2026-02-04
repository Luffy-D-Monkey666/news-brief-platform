# 分类系统重构实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 重构新闻分类系统：删除TCG/海贼王/动漫分类，拆分AI与机器人为AI和具身智能，新增Coding分类

**Architecture:** 按照后端→AI服务→前端的顺序修改，确保数据库schema、AI分类逻辑、前端展示三层完全同步

**Tech Stack:** Node.js (Backend), Python (AI Service), React (Frontend), MongoDB

**安全原则:**
- 每个文件单独修改和测试
- 保持向后兼容（不删除数据库已有数据）
- 使用Git在每个任务后提交
- 测试每层变更后再进入下一层

---

## 变更总结

### 删除的分类
- `tcg_card_game` - TCG信息
- `one_piece` - 海贼王
- `anime_manga` - 动画漫画

### 新增的分类
- `ai_technology` - AI技术
- `embodied_intelligence` - 具身智能
- `coding_development` - Coding开发

### 修改的分类
- `ai_robotics` → 拆分为 `ai_technology` + `embodied_intelligence`

---

## Task 1: 更新后端数据模型

**Files:**
- Modify: `backend/src/models/Brief.js:15-29`

**目标:** 更新MongoDB schema的category enum，删除旧分类，添加新分类

**Step 1: 读取当前模型文件**

```bash
cat backend/src/models/Brief.js
```

**Step 2: 备份原文件**

```bash
cp backend/src/models/Brief.js backend/src/models/Brief.js.backup
```

**Step 3: 修改enum定义**

更新第15-29行的enum数组：

```javascript
enum: [
  'ai_technology',         // AI技术（机器学习、大语言模型、AI应用）
  'embodied_intelligence', // 具身智能（机器人、自动驾驶、物理世界AI）
  'coding_development',    // Coding开发（编程语言、开发工具、开源项目）
  'ev_automotive',         // 新能源汽车
  'finance_investment',    // 投资财经
  'business_tech',         // 商业科技
  'politics_world',        // 政治国际
  'economy_policy',        // 经济政策
  'health_medical',        // 健康医疗
  'energy_environment',    // 能源环境
  'entertainment_sports',  // 娱乐体育
  'general'               // 综合
]
```

**Step 4: 验证语法正确性**

```bash
cd backend && node -c src/models/Brief.js
```

预期输出：无错误（命令成功返回）

**Step 5: 提交变更**

```bash
git add backend/src/models/Brief.js
git commit -m "refactor(backend): 更新分类enum - 删除TCG/OP/动漫，新增AI/具身智能/Coding

- 删除: tcg_card_game, one_piece, anime_manga
- 新增: ai_technology, embodied_intelligence, coding_development
- 拆分原ai_robotics为两个独立分类

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 2: 更新AI服务配置

**Files:**
- Modify: `ai-service/config/settings.py:14-55`

**目标:** 更新CATEGORIES列表和CATEGORY_NAMES映射

**Step 1: 备份配置文件**

```bash
cp ai-service/config/settings.py ai-service/config/settings.py.backup
```

**Step 2: 修改CATEGORIES列表（第14-33行）**

```python
CATEGORIES = [
    # 核心关注领域（最高优先级）
    'ai_technology',         # AI技术
    'embodied_intelligence', # 具身智能
    'coding_development',    # Coding开发
    'ev_automotive',         # 新能源汽车
    'finance_investment',    # 投资财经

    # 主流新闻分类
    'business_tech',         # 商业科技
    'politics_world',        # 政治国际
    'economy_policy',        # 经济政策
    'health_medical',        # 健康医疗
    'energy_environment',    # 能源环境
    'entertainment_sports',  # 娱乐体育
    'general'               # 综合
]
```

**Step 3: 修改CATEGORY_NAMES映射（第36-55行）**

```python
CATEGORY_NAMES = {
    # 核心关注领域
    'ai_technology': 'AI技术',
    'embodied_intelligence': '具身智能',
    'coding_development': 'Coding',
    'ev_automotive': '新能源汽车',
    'finance_investment': '投资财经',

    # 主流新闻分类
    'business_tech': '商业科技',
    'politics_world': '政治国际',
    'economy_policy': '经济政策',
    'health_medical': '健康医疗',
    'energy_environment': '能源环境',
    'entertainment_sports': '娱乐体育',
    'general': '综合'
}
```

**Step 4: 验证Python语法**

```bash
cd ai-service && python -m py_compile config/settings.py
```

预期输出：无错误

**Step 5: 提交变更**

```bash
git add ai-service/config/settings.py
git commit -m "refactor(ai-service): 更新分类配置 - CATEGORIES和CATEGORY_NAMES

- 删除TCG/海贼王/动漫相关分类
- ai_robotics拆分为ai_technology和embodied_intelligence
- 新增coding_development分类

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 3: 更新AI分类Prompt

**Files:**
- Modify: `ai-service/config/settings.py:263-299`

**目标:** 重写CLASSIFY_PROMPT以反映新分类系统

**Step 1: 定位CLASSIFY_PROMPT（第263行开始）**

```bash
sed -n '263,330p' ai-service/config/settings.py
```

**Step 2: 完全替换CLASSIFY_PROMPT内容**

```python
CLASSIFY_PROMPT = """请将以下新闻分类到最合适的类别。必须严格按照优先级和关键词进行分类。

🎯 核心分类（最高优先级）：

1. ai_technology - AI技术
   关键词：ChatGPT, GPT-4, Claude, OpenAI, Anthropic, DeepMind, 大语言模型, LLM,
           机器学习, Machine Learning, 深度学习, Deep Learning, 神经网络,
           AI应用, AI模型, Transformer, 提示工程, prompt engineering,
           AI安全, AI对齐, AGI, 人工智能, artificial intelligence
   判断：任何与AI算法、模型、应用相关的纯软件/算法层面内容

2. embodied_intelligence - 具身智能
   关键词：机器人, robot, 人形机器人, humanoid, 波士顿动力, Boston Dynamics,
           Tesla Bot, Optimus, Figure AI, 1X Technologies,
           自动驾驶, autonomous driving, FSD, 激光雷达, LiDAR,
           工业机器人, 服务机器人, 无人机, drone, 物理AI, embodied AI,
           机械臂, 传感器融合, sensor fusion, SLAM
   判断：AI在物理世界的应用，涉及硬件、传感器、执行器的智能系统

3. coding_development - Coding开发
   关键词：编程, programming, 代码, code, GitHub, GitLab, 开源, open source,
           Python, JavaScript, Rust, Go, TypeScript, React, Vue, Node.js,
           VSCode, IDE, 编辑器, compiler, 编译器, API, SDK,
           开发工具, developer tools, 版本控制, CI/CD, DevOps,
           框架, framework, 库, library, package, npm, pip,
           算法竞赛, LeetCode, 编程语言, programming language
   判断：编程语言、开发工具、开源项目、编程社区相关内容

📌 其他分类：
- ev_automotive: 新能源汽车（Tesla车辆, 比亚迪, 电动车, 充电桩, 电池技术 - 不含自动驾驶AI）
- finance_investment: 投资财经（股票, 加密货币, Bitcoin, 投资, 金融市场）
- business_tech: 商业科技（科技公司, startup, 融资, IPO, 商业新闻）
- politics_world: 政治国际（国际关系, 政府, 选举, 外交）
- economy_policy: 经济政策（GDP, 通胀, 经济政策, 贸易战）
- health_medical: 健康医疗（医疗, 健康, 疾病, 药品, 疫苗）
- energy_environment: 能源环境（能源, 气候变化, 环保, 可再生能源）
- entertainment_sports: 娱乐体育（体育赛事, 电影, 音乐, 明星）
- general: 综合（无法明确分类的其他新闻）

⚠️ 分类规则：
1. 优先匹配核心分类（ai_technology, embodied_intelligence, coding_development）
2. AI类新闻判断标准：
   - 纯算法/模型/软件应用 → ai_technology
   - 涉及机器人/物理世界/硬件 → embodied_intelligence
   - 自动驾驶系统（包含感知/决策/控制） → embodied_intelligence
   - Tesla/电动车的自动驾驶功能 → embodied_intelligence
   - Tesla/电动车的电池/续航/销量 → ev_automotive
3. 编程相关内容必须归入coding_development
4. 如果无法确定，优先选择更具体的分类
5. 只返回分类代码，不要解释

新闻标题: {title}
新闻摘要: {summary}

请返回最合适的分类代码："""
```

**Step 3: 验证修改后的文件**

```bash
cd ai-service && python -m py_compile config/settings.py
```

预期输出：无错误

**Step 4: 提交变更**

```bash
git add ai-service/config/settings.py
git commit -m "refactor(ai-service): 重写CLASSIFY_PROMPT适配新分类系统

- 移除TCG/海贼王/动漫分类规则
- 新增AI技术/具身智能/Coding三大核心分类规则
- 明确AI类新闻的判断标准（算法vs物理世界）
- 优化关键词和判断逻辑

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 4: 更新AI处理器验证逻辑

**Files:**
- Modify: `ai-service/src/processors/cloud_ai_processor.py:221-227`

**目标:** 更新valid_categories列表

**Step 1: 备份处理器文件**

```bash
cp ai-service/src/processors/cloud_ai_processor.py ai-service/src/processors/cloud_ai_processor.py.backup
```

**Step 2: 修改valid_categories列表（第221-227行）**

```python
valid_categories = [
    'ai_technology', 'embodied_intelligence', 'coding_development',
    'ev_automotive', 'finance_investment',
    'business_tech', 'politics_world', 'economy_policy',
    'health_medical', 'energy_environment', 'entertainment_sports',
    'general'
]
```

**Step 3: 验证Python语法**

```bash
cd ai-service && python -m py_compile src/processors/cloud_ai_processor.py
```

预期输出：无错误

**Step 4: 提交变更**

```bash
git add ai-service/src/processors/cloud_ai_processor.py
git commit -m "refactor(ai-service): 更新分类验证列表

- 更新valid_categories以匹配新分类系统
- 删除旧分类，添加新分类

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 5: 更新前端分类过滤器

**Files:**
- Modify: `frontend/src/components/CategoryFilter.js:1-61`

**目标:** 更新categoryIcons和categoryNames，添加新图标

**Step 1: 备份前端组件**

```bash
cp frontend/src/components/CategoryFilter.js frontend/src/components/CategoryFilter.js.backup
```

**Step 2: 更新导入的图标（第1-19行）**

```javascript
import React from 'react';
import {
  FaDollarSign,
  FaMicrochip,
  FaHeartbeat,
  FaLeaf,
  FaCar,
  FaRobot,
  FaBrain,
  FaGlobe,
  FaChartLine,
  FaBolt,
  FaLandmark,
  FaNewspaper,
  FaFilm,
  FaCode,        // 新增：Coding图标
  FaNetworkWired // 新增：具身智能图标（网络连接，象征物理世界互联）
} from 'react-icons/fa';
```

**Step 3: 更新categoryIcons对象（第21-40行）**

```javascript
const categoryIcons = {
  // 核心关注领域（最高优先级）
  ai_technology: { icon: FaBrain, color: 'text-purple-600', highlight: true, special: true },
  embodied_intelligence: { icon: FaRobot, color: 'text-indigo-600', highlight: true, special: true },
  coding_development: { icon: FaCode, color: 'text-blue-600', highlight: true, special: true },
  ev_automotive: { icon: FaBolt, color: 'text-green-600', highlight: true },
  finance_investment: { icon: FaChartLine, color: 'text-red-600', highlight: true },

  // 主流新闻分类
  business_tech: { icon: FaMicrochip, color: 'text-blue-600' },
  politics_world: { icon: FaLandmark, color: 'text-indigo-600' },
  economy_policy: { icon: FaDollarSign, color: 'text-yellow-600' },
  health_medical: { icon: FaHeartbeat, color: 'text-pink-600' },
  energy_environment: { icon: FaLeaf, color: 'text-teal-600' },
  entertainment_sports: { icon: FaFilm, color: 'text-orange-600' },
  general: { icon: FaGlobe, color: 'text-gray-600' }
};
```

**Step 4: 更新categoryNames对象（第42-61行）**

```javascript
const categoryNames = {
  // 核心关注领域
  ai_technology: 'AI技术',
  embodied_intelligence: '具身智能',
  coding_development: 'Coding',
  ev_automotive: '新能源汽车',
  finance_investment: '投资财经',

  // 主流新闻分类
  business_tech: '商业科技',
  politics_world: '政治国际',
  economy_policy: '经济政策',
  health_medical: '健康医疗',
  energy_environment: '能源环境',
  entertainment_sports: '娱乐体育',
  general: '综合'
};
```

**Step 5: 验证React语法**

```bash
cd frontend && npm run build
```

预期输出：构建成功（BUILD SUCCESSFUL）

**Step 6: 提交变更**

```bash
git add frontend/src/components/CategoryFilter.js
git commit -m "refactor(frontend): 更新CategoryFilter分类系统

- 删除TCG/海贼王/动漫分类
- 新增AI技术/具身智能/Coding分类
- 更新图标和中文名称映射
- 保持highlight和special属性

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 6: 更新前端卡片组件

**Files:**
- Modify: `frontend/src/components/BriefCard.js:14-45`

**目标:** 更新categoryColors和categoryNames

**Step 1: 备份卡片组件**

```bash
cp frontend/src/components/BriefCard.js frontend/src/components/BriefCard.js.backup
```

**Step 2: 更新categoryColors对象（第15-29行）**

```javascript
const categoryColors = {
  ai_technology: 'text-purple-600',
  embodied_intelligence: 'text-indigo-600',
  coding_development: 'text-blue-600',
  ev_automotive: 'text-emerald-600',
  finance_investment: 'text-rose-600',
  business_tech: 'text-blue-600',
  politics_world: 'text-indigo-600',
  economy_policy: 'text-yellow-600',
  health_medical: 'text-teal-600',
  energy_environment: 'text-cyan-600',
  entertainment_sports: 'text-orange-600',
  general: 'text-gray-600'
};
```

**Step 3: 更新categoryNames对象（第31-45行）**

```javascript
const categoryNames = {
  ai_technology: 'AI技术',
  embodied_intelligence: '具身智能',
  coding_development: 'Coding',
  ev_automotive: '新能源汽车',
  finance_investment: '投资财经',
  business_tech: '商业科技',
  politics_world: '政治国际',
  economy_policy: '经济政策',
  health_medical: '健康医疗',
  energy_environment: '能源环境',
  entertainment_sports: '娱乐体育',
  general: '综合'
};
```

**Step 4: 验证React语法**

```bash
cd frontend && npm run build
```

预期输出：构建成功

**Step 5: 提交变更**

```bash
git add frontend/src/components/BriefCard.js
git commit -m "refactor(frontend): 更新BriefCard分类映射

- 同步categoryColors和categoryNames与新分类系统
- 确保卡片显示正确的分类标签和颜色

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 7: 清理AI服务RSS源配置（可选）

**Files:**
- Modify: `ai-service/config/settings.py:58-216`

**目标:** 删除TCG/海贼王/动漫相关的RSS源配置

**Step 1: 识别需要删除的RSS源**

```bash
sed -n '58,216p' ai-service/config/settings.py | grep -E "TCG|One Piece|海贼王|anime|manga" -n
```

**Step 2: 删除相关RSS源（约120-215行）**

删除以下部分：
- 第105-165行：TCG相关源（Pokemon, OPCG, Dragon Ball等）
- 第166-182行：One Piece相关源
- 第183-215行：Anime & Manga相关源

保留其他通用新闻源（中国、美国、日本、欧洲、科技、财经等）

**Step 3: 验证Python语法**

```bash
cd ai-service && python -m py_compile config/settings.py
```

预期输出：无错误

**Step 4: 提交变更**

```bash
git add ai-service/config/settings.py
git commit -m "refactor(ai-service): 清理已废弃分类的RSS源

- 删除TCG卡牌相关RSS源（Pokemon/OPCG/Dragon Ball等）
- 删除海贼王专属RSS源
- 删除动漫漫画RSS源
- 保留通用新闻源配置

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 8: 端到端测试

**Files:**
- Test: 完整系统

**目标:** 验证分类系统在所有层面正常工作

**Step 1: 启动后端服务**

```bash
cd backend && npm start
```

预期输出：服务器启动在端口8000

**Step 2: 启动AI服务**

```bash
cd ai-service && python src/main.py
```

预期输出：AI服务启动，连接MongoDB成功

**Step 3: 启动前端开发服务器**

```bash
cd frontend && npm start
```

预期输出：前端启动在端口3000

**Step 4: 测试分类显示**

浏览器访问 `http://localhost:3000`

验证项：
- ✅ 分类过滤器显示新的3个核心分类（AI技术、具身智能、Coding）
- ✅ 不再显示旧分类（TCG、海贼王、动漫）
- ✅ 图标和颜色正确显示
- ✅ 点击分类可以正常切换

**Step 5: 测试新闻分类**

检查AI服务日志中新闻的分类结果：

```bash
tail -f ai-service/logs/classifier.log | grep -E "ai_technology|embodied_intelligence|coding_development"
```

验证项：
- ✅ AI相关新闻正确分类到ai_technology
- ✅ 机器人/自动驾驶新闻正确分类到embodied_intelligence
- ✅ 编程相关新闻正确分类到coding_development

**Step 6: 测试数据库兼容性**

查询数据库确认旧数据不受影响：

```bash
mongosh news-brief --eval "db.briefs.countDocuments({category: {$in: ['tcg_card_game', 'one_piece', 'anime_manga']}})"
```

预期输出：显示旧分类数据的数量（这些数据将保留但不再显示）

**Step 7: 记录测试结果**

创建测试报告：

```bash
cat > docs/plans/2026-02-04-category-refactor-test-results.md << 'EOF'
# 分类系统重构测试结果

## 测试时间
2026-02-04

## 测试项目

### 1. 后端Model验证
- ✅ Brief.js enum更新成功
- ✅ 新分类可以保存到数据库
- ✅ 旧分类数据保持不变

### 2. AI服务验证
- ✅ CATEGORIES和CATEGORY_NAMES同步
- ✅ CLASSIFY_PROMPT包含新分类规则
- ✅ valid_categories列表正确
- ✅ AI分类引擎正常工作

### 3. 前端UI验证
- ✅ CategoryFilter显示新分类
- ✅ 图标和颜色正确
- ✅ BriefCard显示新分类标签
- ✅ 分类切换功能正常

### 4. 集成测试
- ✅ 端到端新闻流转正常
- ✅ 新闻正确分类并显示
- ✅ 无JavaScript/Python错误

## 已知问题
- 旧分类数据（TCG/OP/动漫）仍在数据库中，但前端不再显示
- 如需清理，可运行：`db.briefs.deleteMany({category: {$in: ['tcg_card_game', 'one_piece', 'anime_manga']}})`

## 结论
✅ 分类系统重构成功，所有功能正常
EOF
```

**Step 8: 最终提交**

```bash
git add docs/plans/2026-02-04-category-refactor-test-results.md
git commit -m "test: 分类系统重构测试通过

- 完成端到端测试
- 验证所有层面功能正常
- 记录测试结果

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 9: 推送到远程仓库并部署

**Files:**
- Deploy: 所有变更

**目标:** 将所有变更推送到GitHub并触发自动部署

**Step 1: 查看所有提交**

```bash
git log --oneline -10
```

预期输出：显示8个新提交（Task 1-8）

**Step 2: 推送到远程**

```bash
git push origin main
```

预期输出：推送成功

**Step 3: 监控Render部署**

访问Render Dashboard检查部署状态：
- Backend服务自动重新部署
- AI服务自动重新部署
- Frontend自动重新部署

**Step 4: 验证生产环境**

访问生产URL，验证：
- ✅ 新分类系统生效
- ✅ 旧分类不再显示
- ✅ 新闻正常加载和分类

**Step 5: 完成标记**

```bash
git tag -a v1.1.0-category-refactor -m "分类系统重构完成

- 删除TCG/海贼王/动漫分类
- AI与机器人拆分为AI技术和具身智能
- 新增Coding开发分类
- 优化分类Prompt和图标
"
git push origin v1.1.0-category-refactor
```

---

## 回滚计划（如出现问题）

如果生产环境出现问题，可执行以下回滚步骤：

```bash
# 1. 恢复所有备份文件
cp backend/src/models/Brief.js.backup backend/src/models/Brief.js
cp ai-service/config/settings.py.backup ai-service/config/settings.py
cp ai-service/src/processors/cloud_ai_processor.py.backup ai-service/src/processors/cloud_ai_processor.py
cp frontend/src/components/CategoryFilter.js.backup frontend/src/components/CategoryFilter.js
cp frontend/src/components/BriefCard.js.backup frontend/src/components/BriefCard.js

# 2. 提交回滚
git add .
git commit -m "revert: 回滚分类系统重构"
git push origin main

# 3. 等待自动部署完成
```

---

## 实施注意事项

1. **按顺序执行**: 必须严格按照Task 1→9的顺序执行，不可跳过
2. **测试优先**: 每个Task完成后立即验证语法和逻辑
3. **频繁提交**: 每个Task独立提交，便于追踪和回滚
4. **保留备份**: 所有备份文件在部署成功前不要删除
5. **数据兼容**: 不删除数据库中的旧分类数据，只是前端不再显示
6. **监控日志**: 部署后持续监控AI服务的分类日志，确保新分类规则正确工作

---

## 时间估算

- Task 1-6: 各5-10分钟（代码修改和提交）
- Task 7: 10-15分钟（清理RSS源）
- Task 8: 15-20分钟（完整测试）
- Task 9: 5-10分钟（部署和验证）

**总计**: 60-90分钟

---

## 完成标志

当以下所有项目都✅时，重构完成：

- [ ] 后端enum更新
- [ ] AI服务配置更新
- [ ] AI Prompt重写
- [ ] AI处理器验证逻辑更新
- [ ] 前端过滤器组件更新
- [ ] 前端卡片组件更新
- [ ] RSS源清理
- [ ] 端到端测试通过
- [ ] 生产环境部署成功
- [ ] 新分类系统正常工作
