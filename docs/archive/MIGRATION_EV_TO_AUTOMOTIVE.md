# 数据迁移指南：ev_automotive → automotive

## 📋 迁移说明

将所有 `ev_automotive`（新能源汽车）分类的新闻改为 `automotive`（汽车）。

---

## 🚀 方法1：使用Node.js脚本（推荐）

### 前提条件
- 已安装Node.js
- 已配置MONGODB_URI环境变量

### 执行步骤

1. **进入项目目录**
```bash
cd /Users/xufan3/news-brief-platform
```

2. **运行迁移脚本**
```bash
node scripts/migrate_ev_to_automotive.js
```

3. **查看输出**
脚本会显示：
- 需要迁移的文档数量
- 示例数据（前3条）
- 迁移进度
- 验证结果

### 预期输出示例
```
🔗 连接到MongoDB...
📍 URI: mongodb+srv://****@cluster.mongodb.net/news-brief
✅ MongoDB连接成功

📊 统计数据...
   发现 25 条 ev_automotive 分类的新闻

📄 示例数据（前3条）:
   1. 特斯拉Model 3销量突破100万...
      分类: ev_automotive, 创建时间: 2026-02-04T10:30:00.000Z
   2. 比亚迪发布新款电动车...
      分类: ev_automotive, 创建时间: 2026-02-04T09:15:00.000Z
   3. 丰田宣布混动车战略...
      分类: ev_automotive, 创建时间: 2026-02-04T08:45:00.000Z

🔄 开始迁移...
✅ 迁移完成！
   匹配文档: 25
   更新文档: 25

🔍 验证迁移结果...
   ev_automotive 剩余: 0
   automotive 总数: 25

✅ 数据迁移验证成功！所有数据已成功迁移

📌 数据库连接已关闭
```

---

## 🌐 方法2：MongoDB Atlas Web界面

如果无法运行Node.js脚本，可以直接在MongoDB Atlas执行更新命令。

### 执行步骤

1. **访问MongoDB Atlas**
   - 打开 https://cloud.mongodb.com/
   - 登录账户

2. **选择数据库**
   - 点击 "Browse Collections"
   - 选择数据库：`news-brief`
   - 选择集合：`briefs`

3. **执行更新命令**

   点击顶部的 **"..."** 菜单 → 选择 **"Open MongoDB Shell"**

   或者在 Aggregation 标签中执行：

```javascript
// 查看需要迁移的数量
db.briefs.countDocuments({ category: 'ev_automotive' })

// 查看示例数据（可选）
db.briefs.find({ category: 'ev_automotive' }).limit(3)

// 执行迁移
db.briefs.updateMany(
  { category: 'ev_automotive' },
  { $set: { category: 'automotive' } }
)

// 验证结果
db.briefs.countDocuments({ category: 'ev_automotive' })  // 应该返回 0
db.briefs.countDocuments({ category: 'automotive' })      // 应该显示迁移后的总数
```

---

## ⚠️ 注意事项

1. **备份数据**（可选但推荐）
   - MongoDB Atlas有自动备份
   - 如需手动备份，在Atlas中创建快照

2. **迁移时机**
   - 建议在低流量时段执行
   - 迁移过程通常很快（< 1秒）

3. **回滚方案**
   如果需要回滚（将automotive改回ev_automotive）：
   ```javascript
   db.briefs.updateMany(
     { category: 'automotive' },
     { $set: { category: 'ev_automotive' } }
   )
   ```

4. **不影响前端**
   - 前端已更新为automotive
   - 迁移后立即生效

---

## 📊 验证迁移成功

迁移后，访问网站验证：
1. 刷新网站（Cmd+Shift+R 硬刷新）
2. 点击"汽车"分类
3. 应该能看到之前的"新能源汽车"新闻

---

## 🐛 故障排查

### 问题1：连接失败
**错误**: `MongoError: Authentication failed`

**解决**:
- 检查MONGODB_URI环境变量是否正确
- 确认MongoDB Atlas白名单包含当前IP

### 问题2：找不到文档
**输出**: `发现 0 条 ev_automotive 分类的新闻`

**原因**: 可能已经迁移过，或者没有旧数据

**验证**:
```javascript
db.briefs.countDocuments({ category: 'automotive' })
```

### 问题3：部分未迁移
**输出**: `ev_automotive 剩余: 5`

**解决**: 再次运行脚本，或检查是否有其他进程在写入

---

**创建时间**: 2026-02-04
**迁移类型**: 分类重命名
**影响范围**: 仅 category 字段
**风险级别**: 低（可回滚）
