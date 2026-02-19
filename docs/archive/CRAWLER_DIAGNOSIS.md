# 爬虫状态诊断指南

**问题**: 最新新闻是43分钟前的
**配置**: 应该每2分钟抓取一次
**时间差**: 41分钟没有新新闻 = 约20个抓取周期未执行

---

## 🔍 可能的原因

### 1. AI Service崩溃或未运行 (最可能)
**现象**:
- 服务崩溃后没有重启
- Render上的Worker停止运行

**检查方法**:
```bash
# 方法1: Render Dashboard
1. 访问 https://dashboard.render.com/
2. 找到 "AI Service Worker"
3. 查看状态:
   - ✅ Running (绿色) - 正常
   - ⚠️  Building (黄色) - 部署中
   - ❌ Failed/Stopped (红色) - 已停止

# 方法2: 查看日志
1. 点击 AI Service Worker
2. 点击 "Logs" 标签
3. 查看最后一条日志的时间戳
4. 如果最后日志是43分钟前 → 服务已停止
```

**解决方案**:
- 如果状态是 Failed/Stopped，点击 "Manual Deploy" → "Deploy latest commit"
- 如果持续崩溃，查看错误日志

---

### 2. DeepSeek API失败 (可能性中等)
**现象**:
- 爬虫运行正常，但AI处理100%失败
- 所有新闻被丢弃

**检查方法**:
```bash
# 在Render Logs中搜索
"批量处理完成"

# 正常输出:
批量处理完成: 45/50 (90.0%)  # ✅ 成功率>80%

# 异常输出:
批量处理完成: 0/50 (0.0%)    # ❌ 全部失败
⚠️  高失败率检测: 100.0% 的新闻处理失败
```

**可能原因**:
- DeepSeek API密钥失效
- API配额用完
- API速率限制

**解决方案**:
```bash
# 1. 检查DeepSeek控制台
访问: https://platform.deepseek.com/usage

# 2. 检查余额和配额
- 余额是否充足
- 是否超过每日/每小时限制

# 3. 检查环境变量
Render Dashboard → AI Service → Environment
确认 DEEPSEEK_API_KEY 正确配置
```

---

### 3. MongoDB连接失败 (可能性较低)
**现象**:
- 新闻抓取和处理成功
- 但无法保存到数据库

**检查方法**:
```bash
# 在Render Logs中搜索
"MongoDB"
"pymongo.errors"

# 错误示例:
pymongo.errors.ServerSelectionTimeoutError: connection timeout
```

**解决方案**:
```bash
# 1. 检查MongoDB Atlas
访问: https://cloud.mongodb.com/

# 2. 检查IP白名单
- 确保允许来自任何IP (0.0.0.0/0)
- 或添加Render的IP范围

# 3. 检查连接字符串
Render Dashboard → AI Service → Environment
确认 MONGODB_URI 正确配置
```

---

### 4. RSS源全部失效 (可能性极低)
**现象**:
- 爬虫运行正常
- 但所有RSS源都无法访问

**检查方法**:
```bash
# 在Render Logs中搜索
"步骤 1/5"
"采集到 0 条原始新闻"

# 正常输出:
步骤 1/5: 采集到 150 条原始新闻

# 异常输出:
步骤 1/5: 采集到 0 条原始新闻
```

**解决方案**:
- 检查网络连接
- 测试几个RSS源是否可访问
- 可能是RSSHub服务问题

---

## 🚀 快速诊断步骤

### Step 1: 检查AI Service状态 (30秒)
```bash
1. 访问 https://dashboard.render.com/
2. 找到 AI Service Worker
3. 查看状态指示灯
```

**如果是红色/停止**:
→ 点击 "Manual Deploy" → "Deploy latest commit"
→ 等待5-10分钟部署完成
→ **问题解决**

**如果是绿色/运行中**:
→ 继续Step 2

---

### Step 2: 检查最近日志 (2分钟)
```bash
1. 点击 AI Service Worker
2. 点击 "Logs" 标签
3. 查看最新的日志时间
```

**如果最后日志是43分钟前**:
→ 服务已崩溃但状态未更新
→ 手动重启服务
→ **问题解决**

**如果有最近的日志**:
→ 搜索 "批量处理完成"
→ 检查成功率
→ 继续Step 3

---

### Step 3: 检查处理成功率 (1分钟)
```bash
# 在日志中搜索
"批量处理完成"
```

**如果显示: 0/50 (0.0%)**:
→ AI处理全部失败
→ 检查DeepSeek API状态
→ 检查API密钥和余额

**如果显示: 45/50 (90.0%)**:
→ 处理正常
→ 但新闻没有保存到数据库
→ 检查MongoDB连接

---

### Step 4: 手动触发一次抓取 (高级)
```bash
# 如果有SSH访问权限
cd /opt/render/project/src
python src/main.py

# 观察输出
# 正常输出示例:
新闻简报AI服务启动
AI提供商: deepseek
采集间隔: 120秒
执行首次采集...
步骤 1/5: 从 118 个RSS源采集新闻
步骤 2/5: 采集到 150 条原始新闻
步骤 3/5: 去重后剩余 120 条新闻
步骤 4/5: 批量处理新闻
批量处理完成: 110/120 (91.7%)
步骤 5/5: 成功保存 110/110 条简报
```

---

## 🔧 最可能的解决方案

### 方案1: 重启AI Service (90%有效)
```bash
1. Render Dashboard → AI Service Worker
2. 右上角 Settings → 下拉到底部
3. 点击 "Suspend Service"
4. 等待10秒
5. 点击 "Resume Service"
6. 等待服务重新启动
```

### 方案2: 重新部署 (95%有效)
```bash
1. Render Dashboard → AI Service Worker
2. 右上角点击 "Manual Deploy"
3. 选择 "Deploy latest commit"
4. 等待5-10分钟
5. 查看日志确认正常运行
```

### 方案3: 检查并修复环境变量 (如果是API问题)
```bash
1. Render Dashboard → AI Service Worker
2. Environment 标签
3. 检查以下变量:
   - DEEPSEEK_API_KEY (必需)
   - MONGODB_URI (必需)
   - AI_PROVIDER=deepseek
   - CRAWL_INTERVAL=120
4. 如有修改，保存后会自动重新部署
```

---

## 📊 预期恢复时间

| 问题类型 | 解决时间 | 恢复时间 |
|---------|---------|---------|
| 服务崩溃 | 1分钟（重启） | 立即 |
| 正在部署 | 0分钟（等待） | 5-10分钟 |
| API失败 | 5分钟（充值/修复） | 立即 |
| DB连接失败 | 10分钟（配置） | 立即 |

---

## 🎯 验证修复成功

重启/修复后，2-3分钟内应该看到：

### 1. 日志输出正常
```
批量处理完成: X/Y (>80%)
成功保存 X/X 条简报
```

### 2. 网站有新新闻
```bash
# 刷新网站
Cmd + Shift + R

# 检查最新新闻的时间
应该显示: "几分钟前" 或 "刚刚"
```

### 3. API返回新数据
```bash
curl "https://your-backend.onrender.com/api/briefs?limit=1"

# 检查返回的 created_at 字段
# 应该是最近几分钟的时间
```

---

## 📋 如果问题持续

如果重启后仍然没有新新闻：

1. **导出最近的日志**:
   ```bash
   Render Dashboard → Logs → 复制最后100行
   ```

2. **检查错误模式**:
   - 是否有重复的错误信息
   - 是否有Python异常栈
   - 是否有连接超时

3. **临时解决方案**:
   - 降低CRAWL_INTERVAL到300秒（5分钟）
   - 减少RSS源数量
   - 切换到备用AI provider

---

## 🔗 相关资源

- [Render Dashboard](https://dashboard.render.com/)
- [DeepSeek控制台](https://platform.deepseek.com/)
- [MongoDB Atlas](https://cloud.mongodb.com/)

---

**创建时间**: 2026-02-04
**下次检查**: 修复后2分钟
