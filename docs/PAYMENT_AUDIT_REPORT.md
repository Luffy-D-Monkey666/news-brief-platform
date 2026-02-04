# 系统付费服务审计报告

生成时间：2026-02-04
项目：News Brief Platform

---

## 📊 付费服务总览

### ✅ 当前已确认的付费服务

| 服务类别 | 服务名称 | 费用状态 | 月度费用估算 | 备注 |
|---------|---------|---------|------------|------|
| **AI API** | DeepSeek API | 💰 **需要付费** | ¥10-50/月 | 核心服务，新闻分类和摘要生成 |

### ⚠️ 可能涉及付费的服务（需确认）

| 服务类别 | 服务名称 | 费用状态 | 免费额度 | 超出费用 |
|---------|---------|---------|---------|---------|
| **部署平台** | Render.com | 🆓 免费层可用 | 750小时/月（免费实例） | $7/月起（付费实例） |
| **数据库** | MongoDB Atlas | 🆓 免费层可用 | 512MB存储 | $9/月起（M10实例） |
| **缓存服务** | Redis (Render提供) | 🆓 免费层可用 | 25MB内存 | 需升级Render付费计划 |

---

## 📝 详细分析

### 1. AI API服务 - DeepSeek（✅ 已确认付费）

**配置位置：**
- `ai-service/config/settings.py` - AI_PROVIDER设置
- `render.yaml` - 环境变量 `DEEPSEEK_API_KEY`

**使用情况：**
```python
# 当前配置
AI_PROVIDER = 'deepseek'
DEEPSEEK_MODEL = 'deepseek-chat'
```

**调用频率估算：**
- 爬虫间隔：120秒（2分钟）
- RSS源数量：约32个（删除TCG/动漫后）
- 每个源抓取：20条新闻
- 每条新闻需要2次API调用（分类+摘要）

**月度调用量估算：**
```
每轮抓取: 32源 × 20条 × 2次API = 1,280次调用
每天调用: (24小时 × 60分钟 / 2分钟) × 1,280 = 921,600次
每月调用: 921,600 × 30 = 27,648,000次调用
```

**费用估算（DeepSeek定价）：**
- DeepSeek-Chat输入：¥1/百万tokens
- DeepSeek-Chat输出：¥2/百万tokens
- 平均每次调用：~500 tokens（输入+输出）
- **预计月度费用：¥13.8-27.6元**

**优化建议：**
1. 调整爬虫间隔到180秒（已在配置中） → 节省33%费用
2. 实施缓存机制，避免重复处理相同新闻
3. 考虑仅对新增新闻调用API

---

### 2. Render.com 部署平台

**当前使用服务：**
1. **Backend Web Service** (Node.js)
2. **AI Service Worker** (Python)
3. **Frontend Static Site** (React)

**免费层限制：**
- ✅ 每月750小时免费实例时间
- ✅ 3个免费实例（Backend + AI Worker + Frontend = 3个）
- ✅ 每个实例：512MB RAM
- ❌ 免费实例会在15分钟无活动后休眠（冷启动）

**是否需要付费：**
- **当前状态：可以使用免费层**
- **付费场景：**
  - 如需24/7不休眠 → $7/月/实例 × 3 = $21/月
  - 如需更多RAM/CPU → $25-85/月/实例

**检查方法：**
```bash
# 访问Render Dashboard查看当前计划
open https://dashboard.render.com/
```

**优化建议：**
- 前端使用免费层已足够（静态站点）
- 后端和AI服务如需常驻，考虑付费升级

---

### 3. MongoDB Atlas 数据库

**配置位置：**
- 环境变量：`MONGODB_URI`
- 连接字符串格式：`mongodb+srv://...@cluster0.mongodb.net/...`

**免费层（M0 Sandbox）：**
- ✅ 512MB存储空间
- ✅ 共享RAM
- ✅ 可用于开发和小型应用
- ❌ 无自动备份

**当前使用估算：**
```javascript
// 每条新闻约1KB
// 每天新增：32源 × 20条 = 640条 = ~640KB
// 每月新增：640KB × 30 = 19.2MB
// 512MB可存储约26个月的数据
```

**是否需要付费：**
- **当前状态：免费层足够**
- **付费场景：**
  - 存储超过512MB → $9/月起（M10实例，2GB RAM）
  - 需要自动备份 → $9/月起

**检查方法：**
```bash
# 登录MongoDB Atlas查看当前存储使用情况
open https://cloud.mongodb.com/
```

---

### 4. Redis 缓存服务

**当前使用：**
- WebSocket消息队列
- 实时新闻推送缓存

**Render提供的Redis：**
- ✅ 免费层：25MB内存
- ❌ 需要配合Render付费计划使用
- 💰 付费：$10/月起（100MB）

**是否需要付费：**
- **当前状态：如使用Render Redis，需要升级到Starter计划（$7/月）**
- **免费替代方案：**
  - 使用Redis Labs免费层（30MB）
  - 使用Upstash Redis（10,000次请求/天免费）

---

## 💡 总体费用估算

### 场景A：完全免费配置（功能受限）
| 服务 | 费用 | 说明 |
|-----|------|------|
| DeepSeek API | ¥10-30/月 | **唯一必须付费** |
| Render 免费层 | $0 | 服务会休眠 |
| MongoDB 免费层 | $0 | 512MB存储 |
| Redis Labs免费 | $0 | 30MB内存 |
| **月度总计** | **¥10-30** | **约$1.5-4.5/月** |

### 场景B：稳定运行配置（推荐）
| 服务 | 费用 | 说明 |
|-----|------|------|
| DeepSeek API | ¥10-30/月 | 核心AI服务 |
| Render Starter (3实例) | $21/月 | 24/7运行不休眠 |
| MongoDB 免费层 | $0 | 足够使用 |
| Render Redis | 包含 | Starter计划包含 |
| **月度总计** | **¥10-30 + $21** | **约$24-25/月** |

### 场景C：高性能配置（未来扩展）
| 服务 | 费用 | 说明 |
|-----|------|------|
| DeepSeek API | ¥50-100/月 | 更高调用量 |
| Render Standard | $75/月 | 更多资源 |
| MongoDB M10 | $9/月 | 2GB RAM + 备份 |
| **月度总计** | **¥50-100 + $84** | **约$91-98/月** |

---

## 🔍 如何检查当前费用状态

### 1. 检查DeepSeek API使用情况
```bash
# 访问DeepSeek控制台
open https://platform.deepseek.com/usage
```
- 查看当前余额
- 查看API调用量统计
- 设置月度预算提醒

### 2. 检查Render计费状态
```bash
# 访问Render Dashboard
open https://dashboard.render.com/
```
- 点击右上角头像 → Billing
- 查看当前计划（Free/Starter/Standard）
- 查看本月已使用时长

### 3. 检查MongoDB Atlas存储
```bash
# 访问MongoDB Atlas
open https://cloud.mongodb.com/
```
- 进入Cluster → Metrics
- 查看Storage Used
- 查看Data Size

### 4. 检查Redis使用情况
```bash
# 如使用Render Redis，在Render Dashboard查看
# 如使用Redis Labs，访问：
open https://app.redislabs.com/
```

---

## ⚙️ 成本优化建议

### 立即可行的优化（节省50-70%）

1. **调整爬虫频率**
   ```python
   # 当前：120秒（2分钟）
   # 建议：300秒（5分钟）
   CRAWL_INTERVAL = 300
   # 节省效果：API调用量减少60%，费用降至¥4-12/月
   ```

2. **实施智能缓存**
   ```python
   # 添加新闻去重逻辑
   def is_duplicate(news_url):
       return redis_client.exists(f"processed:{news_url}")

   # 节省效果：避免重复处理，减少30%调用
   ```

3. **使用Render免费层 + 定时唤醒**
   ```bash
   # 使用外部监控服务（UptimeRobot免费版）定期ping
   # 保持服务活跃，避免付费
   ```

### 中期优化（需要开发工作）

4. **本地缓存分类结果**
   ```python
   # 对已分类的新闻标题hash值缓存
   # 相同或相似新闻直接使用缓存分类
   ```

5. **批量处理API调用**
   ```python
   # 将多条新闻合并为一次API调用
   # 利用DeepSeek支持的长上下文
   ```

---

## 📋 检查清单

### 立即检查项（现在就做）
- [ ] 登录DeepSeek平台查看当前余额和使用量
- [ ] 登录Render Dashboard确认当前使用的计划
- [ ] 登录MongoDB Atlas查看存储使用情况
- [ ] 确认Redis服务提供商和费用状态

### 每月检查项
- [ ] DeepSeek API调用量和费用
- [ ] Render实例运行时长
- [ ] MongoDB存储空间使用率
- [ ] 检查是否有意外的付费服务

### 优化任务（可选）
- [ ] 调整CRAWL_INTERVAL到300秒
- [ ] 实施新闻去重缓存机制
- [ ] 设置DeepSeek月度预算告警
- [ ] 考虑使用Upstash Redis替代Render Redis

---

## 🎯 结论与建议

### 当前确认需要付费的服务：
1. **DeepSeek API** - 唯一必须付费的核心服务

### 可能需要付费的服务（取决于使用方式）：
2. **Render.com** - 免费层可用，但有15分钟休眠限制
3. **Redis** - 可使用第三方免费服务替代

### 建议采取的行动：
1. **立即**：登录各平台确认当前费用状态
2. **本周**：实施成本优化措施（调整爬虫间隔）
3. **本月**：监控实际费用，决定是否需要升级Render

### 预计月度费用：
- **最低配置**：¥10-30/月（约$1.5-4.5）
- **推荐配置**：¥10-30 + $21/月（约$24-25）

---

## 📞 相关链接

- [DeepSeek控制台](https://platform.deepseek.com/)
- [Render Dashboard](https://dashboard.render.com/)
- [MongoDB Atlas](https://cloud.mongodb.com/)
- [Redis Labs](https://app.redislabs.com/)
- [Upstash Redis](https://upstash.com/)

---

**报告生成时间**: 2026-02-04
**下次审计建议**: 2026-03-04
