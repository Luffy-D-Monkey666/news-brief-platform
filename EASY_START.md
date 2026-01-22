# 🚀 超简单启动教程

## 📋 开始前准备

### 第一步：安装必需软件

请先安装以下软件（点击链接下载）：

1. **Docker Desktop** （最简单的方式）
   - Mac用户: https://www.docker.com/products/docker-desktop/
   - 下载后双击安装，一路点击"继续"即可

2. **或者** 手动安装以下软件：
   - **Node.js**: https://nodejs.org/ （选择LTS版本）
   - **Python**: https://www.python.org/downloads/ （选择3.9或更高版本）
   - **MongoDB**: https://www.mongodb.com/try/download/community
   - **Redis**: https://redis.io/download/

## 🎯 最简单的启动方法（推荐）

### 使用Docker（3步完成）

```bash
# 1. 进入项目目录
cd /Users/xufan3/news-brief-platform

# 2. 启动所有服务
docker-compose up -d

# 3. 安装AI模型（首次运行需要，大约5分钟）
docker exec -it news-ollama ollama pull qwen2:7b
```

**就这么简单！** 现在打开浏览器访问：

- **📱 网站首页**: http://localhost:3000
- **🔧 后端API**: http://localhost:5000/health

### 停止服务

```bash
cd /Users/xufan3/news-brief-platform
docker-compose down
```

## 📖 详细教程（如果Docker方式失败）

### Mac用户（使用Homebrew）

#### 1. 安装Homebrew（如果还没有）
打开终端，复制粘贴以下命令：
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. 安装所有依赖
```bash
# 安装Node.js、Python、MongoDB、Redis
brew install node python@3.9 mongodb-community redis

# 启动MongoDB和Redis
brew services start mongodb-community
brew services start redis
```

#### 3. 安装Ollama（AI引擎）
```bash
# 下载安装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 下载AI模型（选一个，推荐qwen2）
ollama pull qwen2:7b
# 或者
ollama pull llama3
```

#### 4. 启动项目
```bash
cd /Users/xufan3/news-brief-platform

# 使用一键启动脚本
bash start-dev.sh
```

#### 5. 打开浏览器
访问: http://localhost:3000

## 🔗 重要链接

### 官方下载链接

| 软件 | 下载地址 | 说明 |
|------|---------|------|
| Docker Desktop (Mac) | https://desktop.docker.com/mac/main/arm64/Docker.dmg | M1/M2芯片Mac |
| Docker Desktop (Intel Mac) | https://desktop.docker.com/mac/main/amd64/Docker.dmg | Intel芯片Mac |
| Node.js | https://nodejs.org/dist/v18.18.0/node-v18.18.0.pkg | LTS版本 |
| Python | https://www.python.org/ftp/python/3.9.18/python-3.9.18-macos11.pkg | Python 3.9 |
| MongoDB Compass | https://www.mongodb.com/try/download/compass | 数据库管理工具 |
| Ollama | https://ollama.com/download | AI模型运行环境 |

### 在线教程和文档

- **Ollama官网**: https://ollama.com/
- **Ollama模型库**: https://ollama.com/library
- **Docker入门教程**: https://docs.docker.com/get-started/
- **Node.js官方文档**: https://nodejs.org/docs/latest/api/
- **MongoDB教程**: https://www.mongodb.com/docs/manual/tutorial/getting-started/

### 常用命令参考

```bash
# 检查软件是否安装成功
node --version        # 应该显示 v18.x.x
python3 --version     # 应该显示 Python 3.9.x
mongo --version       # 应该显示 MongoDB 版本
redis-cli --version   # 应该显示 Redis 版本
docker --version      # 应该显示 Docker 版本

# 查看服务状态
brew services list    # 查看所有服务状态

# 启动/停止MongoDB
brew services start mongodb-community
brew services stop mongodb-community

# 启动/停止Redis
brew services start redis
brew services stop redis

# 查看Docker容器
docker ps             # 查看运行中的容器
docker-compose logs   # 查看日志
```

## 🎥 界面预览

启动成功后，你会看到：

1. **首页** (http://localhost:3000)
   - 顶部：标题和连接状态指示器
   - 中间：8个分类按钮（财经、科技、健康等）
   - 下方：新闻简报卡片流

2. **简报卡片包含**：
   - 分类标签（带颜色）
   - 新闻标题
   - AI提炼的简报（50-100字）
   - 来源信息
   - 原文链接按钮

3. **实时更新**：
   - 右上角显示"实时连接中"（绿色）
   - 新简报出现时会有动画效果
   - 带"NEW"标记

## ❓ 常见问题

### Q1: Docker命令找不到？
**A**: 确保Docker Desktop已安装并启动，在菜单栏应该能看到Docker图标

### Q2: 端口被占用？
**A**: 执行以下命令查看和释放端口
```bash
# 查看占用3000端口的进程
lsof -i :3000

# 杀死进程（替换PID为实际进程号）
kill -9 PID
```

### Q3: 网页打不开？
**A**:
1. 等待1-2分钟让服务完全启动
2. 检查Docker容器是否都在运行：`docker ps`
3. 查看日志：`docker-compose logs`

### Q4: 没有新闻显示？
**A**:
1. 首次启动需要等待5-10分钟进行新闻采集
2. 检查AI服务日志：`docker logs news-ai-service`
3. 确保网络连接正常

### Q5: AI处理太慢？
**A**:
1. 考虑使用更小的模型：`ollama pull qwen2:1.5b`
2. 如果有GPU，确保Docker配置了GPU支持
3. 增加系统内存分配

## 📞 获取帮助

如果遇到问题：

1. **查看日志**
   ```bash
   # Docker方式
   docker-compose logs -f

   # 手动启动方式
   # 查看对应终端的输出
   ```

2. **重启服务**
   ```bash
   # Docker方式
   docker-compose restart

   # 手动方式
   # 按Ctrl+C停止，然后重新运行启动命令
   ```

3. **完全清理重启**
   ```bash
   docker-compose down -v  # 删除所有容器和数据
   docker-compose up -d    # 重新启动
   ```

## 🎉 成功标志

当你看到以下内容，说明系统运行正常：

1. ✅ 浏览器能打开 http://localhost:3000
2. ✅ 页面右上角显示"实时连接中"（绿色）
3. ✅ 可以点击不同分类按钮
4. ✅ 等待5-10分钟后，能看到新闻简报卡片

**恭喜！你的实时新闻简报平台已经运行成功了！** 🎊

## 💡 使用小贴士

1. **选择感兴趣的分类**: 点击顶部的分类按钮（财经、科技等）
2. **查看新闻详情**: 点击卡片上的"查看原文"按钮
3. **刷新内容**: 点击右上角的刷新按钮
4. **实时更新**: 保持页面打开，新闻会自动推送

## 🔄 更新和维护

### 更新AI模型
```bash
# 下载新版本模型
docker exec -it news-ollama ollama pull qwen2:latest

# 或切换到其他模型
docker exec -it news-ollama ollama pull llama3
```

### 清理旧数据
```bash
# 进入MongoDB容器
docker exec -it news-mongodb mongosh

# 删除旧新闻（保留最近7天）
use news-brief
db.news.deleteMany({
  created_at: { $lt: new Date(Date.now() - 7*24*60*60*1000) }
})
```

---

**现在就开始吧！只需要3个命令：** 🚀

```bash
cd /Users/xufan3/news-brief-platform
docker-compose up -d
docker exec -it news-ollama ollama pull qwen2:7b
```

然后打开: http://localhost:3000

祝使用愉快！ 📰✨
