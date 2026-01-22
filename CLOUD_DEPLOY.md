# 云端部署指南 - 3种简单方案

本指南提供3种免费或低成本的云端部署方案，**不需要在本地安装任何软件**。

---

## 🌟 方案1：Railway（最推荐，最简单）

**优点**：
- ✅ 完全免费（每月500小时免费额度）
- ✅ 一键部署，5分钟搞定
- ✅ 自动配置数据库
- ✅ 自动HTTPS证书
- ✅ 自动备份

**缺点**：
- ⚠️ 需要绑定信用卡（不会扣费）
- ⚠️ AI功能需要使用云端API（OpenAI/Claude）

### 步骤1：准备Railway账号

1. 访问：https://railway.app/
2. 点击 "Start a New Project"
3. 使用GitHub登录（推荐）

### 步骤2：上传代码到GitHub

```bash
cd /Users/xufan3/news-brief-platform

# 初始化Git仓库
git init
git add .
git commit -m "Initial commit"

# 在GitHub创建新仓库，然后推送
# 访问 https://github.com/new 创建仓库
git remote add origin https://github.com/你的用户名/news-brief-platform.git
git branch -M main
git push -u origin main
```

### 步骤3：在Railway部署

1. 在Railway点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 选择你刚才创建的仓库
4. Railway会自动检测并部署

### 步骤4：添加数据库

1. 点击 "New" → "Database" → "Add MongoDB"
2. 点击 "New" → "Database" → "Add Redis"
3. Railway会自动连接数据库

### 步骤5：配置环境变量

在后端服务中添加以下环境变量：

```
NODE_ENV=production
MONGODB_URI=${{MongoDB.MONGO_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
FRONTEND_URL=你的前端URL
OPENAI_API_KEY=你的API密钥（如果使用OpenAI）
```

### 步骤6：获取URL并访问

部署完成后，Railway会提供两个URL：
- 前端URL：`https://your-app.railway.app`
- 后端URL：`https://your-api.railway.app`

🎉 完成！直接访问前端URL即可使用！

---

## 🚀 方案2：Vercel + Supabase（完全免费）

**优点**：
- ✅ 100%免费
- ✅ 无需信用卡
- ✅ 全球CDN加速
- ✅ 自动HTTPS

**缺点**：
- ⚠️ 需要改用Supabase数据库
- ⚠️ 后端需要改成Serverless函数

### 步骤1：部署前端到Vercel

1. 访问：https://vercel.com/
2. 使用GitHub登录
3. 点击 "Import Project"
4. 选择你的GitHub仓库
5. 设置根目录为 `frontend`
6. 点击 "Deploy"

### 步骤2：部署后端到Vercel

1. 再次点击 "Import Project"
2. 选择同一个仓库
3. 设置根目录为 `backend`
4. 添加环境变量：
   ```
   MONGODB_URI=你的MongoDB URL
   REDIS_URL=你的Redis URL
   ```
5. 点击 "Deploy"

### 步骤3：使用云数据库

**MongoDB：**
1. 访问 https://www.mongodb.com/cloud/atlas
2. 注册免费账号（512MB免费）
3. 创建集群并获取连接URL

**Redis：**
1. 访问 https://upstash.com/
2. 注册免费账号
3. 创建Redis数据库并获取URL

### 步骤4：配置AI服务

由于Vercel不支持长时间运行的进程，需要使用云端AI API：

**选项A：OpenAI（推荐）**
1. 访问：https://platform.openai.com/
2. 注册并获取API密钥
3. 在环境变量中添加：`OPENAI_API_KEY=你的密钥`

**选项B：Claude API**
1. 访问：https://console.anthropic.com/
2. 获取API密钥

🎉 完成！访问Vercel提供的URL即可！

---

## 💰 方案3：阿里云/腾讯云（国内最快）

**优点**：
- ✅ 访问速度快（国内服务器）
- ✅ 中文支持好
- ✅ 可以运行完整的Docker

**缺点**：
- ⚠️ 需要付费（约50-100元/月）
- ⚠️ 需要域名备案

### 步骤1：购买服务器

**阿里云：**
1. 访问：https://www.aliyun.com/product/ecs
2. 选择"轻量应用服务器"（最便宜）
3. 配置：2核4GB，50GB硬盘（约60元/月）

**腾讯云：**
1. 访问：https://cloud.tencent.com/product/lighthouse
2. 选择"轻量应用服务器"
3. 配置：2核4GB（新用户有优惠）

### 步骤2：连接到服务器

```bash
# 使用SSH连接（阿里云/腾讯云会提供IP和密码）
ssh root@你的服务器IP
```

### 步骤3：安装Docker

```bash
# 安装Docker
curl -fsSL https://get.docker.com | sh

# 启动Docker
systemctl start docker
systemctl enable docker
```

### 步骤4：上传并运行项目

```bash
# 在服务器上克隆代码
git clone https://github.com/你的用户名/news-brief-platform.git
cd news-brief-platform

# 启动服务
docker-compose up -d

# 下载AI模型
docker exec -it news-ollama ollama pull qwen2:7b
```

### 步骤5：配置域名（可选）

1. 在域名提供商解析域名到服务器IP
2. 安装Nginx反向代理
3. 配置SSL证书（Let's Encrypt免费）

🎉 完成！访问你的域名或IP即可！

---

## 📊 方案对比

| 特性 | Railway | Vercel | 阿里云/腾讯云 |
|------|---------|--------|---------------|
| **价格** | 免费 | 免费 | 50-100元/月 |
| **难度** | ⭐ 最简单 | ⭐⭐ 简单 | ⭐⭐⭐ 中等 |
| **速度** | 中等 | 快 | 最快（国内） |
| **AI功能** | 需要API | 需要API | 完整支持 |
| **数据库** | 自动配置 | 需要第三方 | 完整支持 |
| **部署时间** | 5分钟 | 10分钟 | 30分钟 |

---

## 🎯 我的推荐

### 如果你想快速体验：
**选择Railway** - 5分钟搞定，完全免费

### 如果你想100%免费：
**选择Vercel** - 需要一些配置，但永久免费

### 如果你想要最好的性能：
**选择阿里云/腾讯云** - 需要付费，但速度最快，功能完整

---

## 🔧 需要修改的代码

无论选择哪个方案，我都已经准备好了对应的配置文件。你只需要：

1. **告诉我你选择哪个方案**
2. **我会帮你修改AI服务部分**（使用云端API替代本地Ollama）
3. **我会提供详细的部署命令**

---

## 💡 关于AI功能的说明

由于云端平台限制，需要将本地AI改为云端API：

### OpenAI API（推荐）
- **价格**：$0.002/1K tokens（约0.015元人民币）
- **速度**：快
- **中文支持**：好
- **注册**：https://platform.openai.com/

### Claude API
- **价格**：$0.008/1K tokens
- **速度**：快
- **中文支持**：很好
- **注册**：https://console.anthropic.com/

### 成本估算
- 每条新闻约500 tokens
- 100条新闻约 $0.1（约0.7元人民币）
- 每天处理1000条新闻约 7元人民币

---

## 📞 下一步

**请告诉我：**
1. 你选择哪个方案？（Railway / Vercel / 阿里云）
2. AI部分想用OpenAI还是Claude？
3. 你有GitHub账号吗？

告诉我后，我会：
1. ✅ 修改代码以使用云端API
2. ✅ 提供详细的部署命令
3. ✅ 创建一键部署脚本
4. ✅ 帮你解决部署中的问题

让我知道你的选择，我们继续！🚀
