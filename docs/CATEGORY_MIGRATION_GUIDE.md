# 分类迁移指南：coding_development → ai_programming

## 概述

已完成代码层面的分类重命名（从 `coding_development` 改为 `ai_programming`），但数据库中已有的旧分类数据需要手动迁移。

## 迁移影响

- **需要迁移**：数据库中所有 `category: 'coding_development'` 的新闻文档
- **目标分类**：`category: 'ai_programming'`
- **风险等级**：低（只修改分类字段，不影响其他数据）

## 迁移方法

### 方法1：使用迁移脚本（推荐）

已创建迁移脚本：`backend/scripts/migrate_category_coding_to_ai_programming.js`

**在生产环境运行：**

```bash
# 1. 进入backend目录
cd backend

# 2. 确保环境变量已配置（MONGODB_URI）
# 如果使用Render.com，环境变量已自动配置
# 如果本地运行，需要先创建 .env 文件

# 3. 运行迁移脚本
node scripts/migrate_category_coding_to_ai_programming.js
```

**预期输出：**

```
连接MongoDB...
MongoDB 已连接

找到 X 条 'coding_development' 分类的新闻

开始迁移...

迁移完成！
- 匹配文档数：X
- 修改文档数：X

验证结果：
- 剩余 'coding_development'：0 条（应为0）
- 新增 'ai_programming'：X 条

✅ 迁移成功！所有数据已更新

数据库连接已关闭
```

### 方法2：使用MongoDB Shell

如果你有MongoDB Atlas访问权限，可以直接在MongoDB Shell中执行：

```javascript
// 连接到数据库
use news-brief

// 查看需要迁移的数据量
db.briefs.countDocuments({ category: 'coding_development' })

// 执行迁移
db.briefs.updateMany(
  { category: 'coding_development' },
  { $set: { category: 'ai_programming' } }
)

// 验证迁移结果
db.briefs.countDocuments({ category: 'coding_development' })  // 应该为 0
db.briefs.countDocuments({ category: 'ai_programming' })
```

### 方法3：在Render.com运行迁移

1. 登录Render Dashboard
2. 进入Backend Web Service
3. 点击 **Shell** 标签
4. 运行命令：
   ```bash
   node scripts/migrate_category_coding_to_ai_programming.js
   ```

## 迁移前检查清单

- [ ] 已部署最新代码到生产环境
- [ ] 确认Backend、AI Service、Frontend三个服务都已更新
- [ ] 备份数据库（可选，MongoDB Atlas通常有自动备份）

## 迁移后验证

### 1. 检查前端分类显示

访问网站，确认：
- 分类筛选器中显示 **"AI编程"** 而不是 "Coding"
- 点击 "AI编程" 分类能正确显示新闻
- 旧的 coding_development 新闻已显示在 "AI编程" 分类下

### 2. 检查新抓取的新闻

等待爬虫下一轮抓取（约2分钟），确认：
- 关于Claude Code、Cursor、Copilot的新闻被分类到 "AI编程"
- 传统编程相关新闻（GitHub、Dev.to等）也被分类到 "AI编程"

### 3. API接口测试

```bash
# 获取 ai_programming 分类的新闻
curl https://your-backend.onrender.com/api/briefs?category=ai_programming

# 确认返回数据正常
```

## 回滚方案

如果迁移后发现问题，可以回滚：

```javascript
// 在MongoDB Shell中执行
db.briefs.updateMany(
  { category: 'ai_programming' },
  { $set: { category: 'coding_development' } }
)
```

然后回滚代码到上一个commit：
```bash
git revert HEAD
git push
```

## 常见问题

### Q1: 迁移脚本连接不到数据库？
**A:** 确保 MONGODB_URI 环境变量已正确配置。在Render.com上，环境变量应该已自动配置。

### Q2: 迁移后前端还是显示 "Coding"？
**A:** 清除浏览器缓存，或强制刷新页面（Ctrl+Shift+R 或 Cmd+Shift+R）

### Q3: 旧的 coding_development 新闻还能访问吗？
**A:** 迁移后，这些新闻的分类字段会变成 `ai_programming`，可以通过 "AI编程" 分类访问。

### Q4: 需要重启服务吗？
**A:** 不需要。迁移只修改数据，不影响运行中的服务。

## 技术细节

### 修改的文件

- `ai-service/config/settings.py` - CATEGORIES、CATEGORY_NAMES、CLASSIFY_PROMPT
- `backend/src/models/Brief.js` - MongoDB schema enum
- `frontend/src/components/CategoryFilter.js` - categoryIcons、categoryNames
- `frontend/src/components/BriefCard.js` - categoryColors、categoryNames

### 数据库Schema变更

```javascript
// 旧Schema
enum: ['ai_technology', 'embodied_intelligence', 'coding_development', ...]

// 新Schema
enum: ['ai_technology', 'embodied_intelligence', 'ai_programming', ...]
```

### 新增的分类关键词

AI编程工具：Claude Code, Cursor, GitHub Copilot, Kimi Code, OpenClaw, Windsurf, Aider, Replit AI, Tabnine, Codeium, AI Agent, Code Agent, 代码助手, 智能编程, AI代码生成, AI辅助编程

---

**创建时间**: 2026-02-04
**Commit**: 2fc7800 - feat: rename 'coding_development' to 'ai_programming' category
