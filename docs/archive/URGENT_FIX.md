# 🚨 紧急问题：AI Service未生成中文简报

## 问题现状

数据库中有157条简报，但**全部是英文/德文原文**，没有经过AI翻译！

示例：
- 标题: `Donald-Trump-Rede in Davos: China widerlegt Windkraft-Aussagen` (德文)
- 摘要: `Trump stellt Behauptungen auf...` (德文)

**这不是我们要的中文简报！**

---

## 根本原因分析

AI Service的流程应该是：
```
爬取RSS → AI翻译成中文 → 保存到数据库
```

但实际发生的是：
```
爬取RSS → 跳过AI处理 → 直接保存原文
```

**最可能的原因**: Render上的`OPENAI_API_KEY`环境变量**没有设置**或**设置错误**

---

## 🔧 立即修复步骤

### 步骤1: 检查Render环境变量

1. 访问 https://dashboard.render.com
2. 找到 `ai-service`
3. 点击 "Environment"标签
4. 检查是否有 `OPENAI_API_KEY`

**如果没有或者是空的，这就是问题所在！**

### 步骤2: 设置正确的API Key

在Render的Environment页面添加：

```
Key: OPENAI_API_KEY
Value: sk-proj-xxxxx... (你的OpenAI API Key)
```

**如果没有API Key**:
1. 访问 https://platform.openai.com/api-keys
2. 登录你的OpenAI账号
3. 点击"Create new secret key"
4. 复制生成的key (sk-proj-xxxxx...)
5. 粘贴到Render环境变量

### 步骤3: 重启AI Service

设置好环境变量后：
1. 点击 "Manual Deploy" → "Deploy latest commit"
2. 或者点击右上角的 "Restart" 按钮

### 步骤4: 等待生成新简报

- AI Service重启后会立即爬取
- 约10-15分钟后会有新的中文简报
- 刷新前端页面查看

---

## 🔍 如何验证修复成功

### 方法1: 查看Render日志

在AI Service的Logs标签，应该看到：

✅ **正确的日志** (有AI处理):
```
从 https://feeds.bbci.co.uk... 爬取到 10 条新闻
开始AI处理...
处理完成: [politics_world] 英国首相宣布... (中文标题)
处理完成: [ai_robotics] OpenAI发布新模型... (中文标题)
成功保存 XXX 条简报
```

❌ **错误的日志** (跳过AI):
```
从 https://feeds.bbci.co.uk... 爬取到 10 条新闻
摘要生成失败: ... (大量这样的错误)
或直接跳过AI处理
```

### 方法2: 检查数据库

运行检查脚本：
```python
python3 -c "
from pymongo import MongoClient

MONGODB_URI = 'mongodb+srv://newsuser:16800958@cluster0.qrke26f.mongodb.net/news-brief?retryWrites=true&w=majority&appName=Cluster0'

client = MongoClient(MONGODB_URI)
db = client['news-brief']
briefs = db['briefs']

latest = briefs.find_one({}, sort=[('created_at', -1)])
print(f'标题: {latest.get(\"title\")}')
print(f'摘要: {latest.get(\"summary\")[:100]}')
"
```

**期望输出** (中文):
```
标题: OpenAI发布GPT-5模型
摘要: 美国人工智能公司OpenAI今天正式发布了新一代大语言模型GPT-5。据悉，该模型在多项基准测试中...
```

---

## 💡 临时方案（如果没有OpenAI API Key）

### 方案A: 使用Claude API (推荐)

如果有Claude API Key:
1. 在Render环境变量添加:
   ```
   CLAUDE_API_KEY=sk-ant-xxxxx...
   AI_PROVIDER=claude
   ```
2. 重启服务

### 方案B: 申请OpenAI API Key

1. 访问 https://platform.openai.com
2. 注册/登录
3. 充值至少$5 USD
4. 创建API Key
5. 添加到Render

---

## 📋 完整诊断检查清单

在Render Dashboard检查以下项目：

### AI Service配置检查
- [ ] `OPENAI_API_KEY` 是否存在？
- [ ] Key是否以`sk-proj-`开头？
- [ ] Key是否完整（很长的字符串）？
- [ ] `MONGODB_URI` 是否正确？
- [ ] `REDIS_URL` 是否正确？

### 服务状态检查
- [ ] AI Service状态是否为"Live"？
- [ ] 最近的部署是否成功？
- [ ] Logs中是否有错误信息？

### OpenAI账号检查
- [ ] 账号是否有余额？
- [ ] API Key是否激活？
- [ ] 是否有使用配额？

---

## ⚠️ 常见错误

### 错误1: API Key格式错误
```
❌ OPENAI_API_KEY=openai-api-key (错误)
✅ OPENAI_API_KEY=sk-proj-xxxxx... (正确)
```

### 错误2: API Key包含空格
```
❌ OPENAI_API_KEY= sk-proj-xxxxx... (前面有空格)
✅ OPENAI_API_KEY=sk-proj-xxxxx... (没有空格)
```

### 错误3: 账号余额不足
OpenAI账号需要有余额才能调用API。检查：
https://platform.openai.com/usage

---

## 🎯 预期最终效果

修复后，前端应显示：

```
┌─────────────────────────────────────┐
│ [图片] (如果有)                      │
├─────────────────────────────────────┤
│ 🏷️ 政治国际                         │
│                                     │
│ 英国首相宣布新经济政策               │  ← 中文标题
│                                     │
│ 英国首相里希·苏纳克今天在议会宣布   │  ← 中文摘要
│ 了一系列新的经济刺激措施，旨在应对   │
│ 通胀压力和经济放缓。新政策包括减税、 │
│ 增加基础设施投资和支持中小企业...   │
│                                     │
│ 🔗 来源: BBC      ⏰ 5分钟前         │
│                                     │
│ [查看原文 →]                         │
└─────────────────────────────────────┘
```

---

## 📞 需要帮助？

如果按照以上步骤操作后仍然有问题：

1. 查看AI Service的完整日志
2. 截图Render的Environment配置
3. 告诉我具体的错误信息

我会继续帮你诊断和修复！

---

**当前状态**: ❌ AI未工作，需要设置OPENAI_API_KEY
**修复时间**: 设置后约15分钟可看到中文简报
**已清空数据**: 是（等待新的中文简报）
