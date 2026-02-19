# 实时诊断脚本 - 检查RSS源和AI处理状态

请在Render Dashboard的AI Service Shell中运行以下命令：

## 1. 检查最近一轮的完整日志
```bash
# 查看最近500行日志，聚焦关键步骤
tail -500 /var/log/*.log | grep "步骤"

# 或者直接查看实时日志
# 在Render Dashboard → AI Service → Logs
# 搜索: "步骤 5/5"
```

**预期输出**:
```
步骤 1/5 完成: 爬取到 659 条新闻
步骤 2/5 完成: 过滤后剩余 57 条新新闻
步骤 3/5 完成: 已保存 57 条原始新闻
步骤 4/5 完成: AI处理完成 XX 条 (成功率: XX%)
步骤 5/5 完成: 成功保存 XX/XX 条简报
```

**关键指标**:
- 步骤4的成功率应该 >80%
- 步骤5的保存数量应该 = 步骤4的处理数量

---

## 2. 测试失效的RSS源

很多重要RSS源返回0条，需要验证：

### 测试CNN RSS
```bash
curl -I https://rss.cnn.com/rss/edition.rss
```

**如果返回 404/403** → RSS URL已失效，需要更新

### 测试Reuters RSS
```bash
curl -I https://www.reuters.com/rssFeed/worldNews
curl -I https://www.reuters.com/rssFeed/technologyNews
```

**如果返回 404** → Reuters更改了RSS结构

### 测试RSSHub源
```bash
curl -I https://rsshub.app/sina/finance
curl -I https://rsshub.app/thepaper/featured
```

**如果返回 5xx错误** → RSSHub服务不稳定

---

## 3. 检查AI编程分类是否有新闻

### 方法1: 数据库查询
```javascript
// 在Render Backend Shell或MongoDB Shell
db.briefs.find({ category: 'ai_programming' }).count()

// 如果 > 0，说明分类成功了
// 如果 = 0，继续诊断
```

### 方法2: API测试
```bash
curl "https://your-backend.onrender.com/api/briefs?category=ai_programming&limit=5"
```

### 方法3: 检查最近的所有分类
```javascript
// 看看最近的新闻都被分到哪些类别
db.briefs.find().sort({ created_at: -1 }).limit(20).forEach(function(doc) {
  print(doc.category + ": " + doc.title.substring(0, 50));
});
```

---

## 4. 查看分类分布统计

```javascript
// MongoDB Shell
db.briefs.aggregate([
  { $group: { _id: "$category", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
]);
```

**预期输出**:
```javascript
{ _id: "politics_world", count: 150 }
{ _id: "business_tech", count: 80 }
{ _id: "ai_technology", count: 60 }
{ _id: "ai_programming", count: ?? }  // 应该 > 0
// ...
```

---

## 🚨 如果ai_programming还是0

### 可能原因A: RSS源都没有编程新闻
检查我们添加的编程类RSS源是否有内容：

```bash
# 测试GitHub Blog
curl https://github.blog/feed/ | grep "<item>" | wc -l

# 测试Dev.to
curl https://dev.to/feed | grep "<item>" | wc -l

# 测试Hacker News
curl https://rsshub.app/hackernews/best | grep "<item>" | wc -l
```

### 可能原因B: 关键词匹配仍然不够
检查最近处理的新闻中，是否有编程相关但被分到其他类别：

```javascript
// 查找标题包含"code", "GitHub", "programming"的新闻
db.briefs.find({
  $or: [
    { title: /code/i },
    { title: /github/i },
    { title: /programming/i }
  ]
}).sort({ created_at: -1 }).limit(10).forEach(function(doc) {
  print(doc.category + ": " + doc.title);
});
```

### 可能原因C: DeepSeek分类逻辑问题
需要查看完整的处理日志，看是否有：
```
处理完成: [ai_programming] XXX
```

---

## 📋 快速操作清单

### 立即执行（5分钟）
1. [ ] 在Render Logs搜索 "步骤 5/5" 查看最终保存数量
2. [ ] 在Render Logs搜索 "[ai_programming]" 查看是否有分类成功
3. [ ] 测试3-5个失效的RSS源（CNN, Reuters等）

### 如果ai_programming还是0（10分钟）
4. [ ] 运行数据库分类分布查询
5. [ ] 搜索标题包含"code/github/programming"的新闻
6. [ ] 检查这些新闻被分到了哪个类别

### 后续优化（1小时）
7. [ ] 替换失效的RSS源
8. [ ] 进一步调整关键词优先级
9. [ ] 考虑手动测试DeepSeek分类几条真实新闻

---

**创建时间**: 2026-02-04
**建议优先级**: 先完成"立即执行"清单，确认问题根源
