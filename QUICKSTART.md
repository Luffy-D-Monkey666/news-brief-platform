# 快速启动指南

## 前置要求

### 必需
- Node.js 18+
- Python 3.9+
- MongoDB 6+
- Redis 7+

### macOS安装依赖
```bash
# 使用Homebrew安装
brew install node python mongodb-community redis

# 启动服务
brew services start mongodb-community
brew services start redis
```

### Ubuntu/Linux安装依赖
```bash
# MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org

# Redis
sudo apt install -y redis-server

# 启动服务
sudo systemctl start mongod
sudo systemctl start redis
```

## 方式一：使用Docker（推荐）

最简单的方式，一键启动所有服务：

```bash
cd news-brief-platform

# 首次运行需要下载Ollama模型
docker-compose up -d ollama
docker exec -it news-ollama ollama pull qwen2:7b

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

访问：
- 前端: http://localhost:3000
- 后端API: http://localhost:5000
- API文档: http://localhost:5000/health

## 方式二：手动启动

### 1. 安装Ollama和模型

```bash
# 安装Ollama
bash setup-ollama.sh

# 或手动安装
curl -fsSL https://ollama.com/install.sh | sh

# 拉取中文优化模型（推荐）
ollama pull qwen2:7b

# 或使用Llama 3
ollama pull llama3

# 启动Ollama服务
ollama serve
```

### 2. 使用启动脚本（推荐）

```bash
# 给脚本执行权限
chmod +x start-dev.sh

# 一键启动所有服务
bash start-dev.sh
```

### 3. 手动分别启动各服务

#### 终端1: 启动AI服务
```bash
cd ai-service

# 创建环境变量
cp .env.example .env

# 安装依赖
pip install -r requirements.txt

# 启动服务
python src/main.py
```

#### 终端2: 启动后端服务
```bash
cd backend

# 创建环境变量
cp .env.example .env

# 安装依赖
npm install

# 启动服务
npm run dev
```

#### 终端3: 启动前端服务
```bash
cd frontend

# 创建环境变量
cp .env.example .env

# 安装依赖
npm install

# 启动服务
npm start
```

## 验证安装

1. 访问前端: http://localhost:3000
2. 检查WebSocket连接状态（页面右上角应显示"实时连接中"）
3. 等待5分钟左右，系统会自动抓取新闻并显示

## 配置说明

### AI服务配置 (ai-service/.env)

```bash
# 使用中文优化模型（推荐）
MODEL_NAME=qwen2:7b

# 或使用Llama 3
# MODEL_NAME=llama3

# 调整爬取频率（秒）
CRAWL_INTERVAL=300  # 5分钟
```

### 添加更多新闻源

编辑 `ai-service/config/settings.py`：

```python
NEWS_SOURCES = {
    'rss_feeds': [
        # 添加你的RSS源
        'https://your-news-site.com/rss',
    ]
}
```

## 常见问题

### 1. Ollama连接失败
```bash
# 检查Ollama服务状态
curl http://localhost:11434/api/tags

# 重启Ollama
pkill ollama
ollama serve
```

### 2. MongoDB连接失败
```bash
# 检查MongoDB状态
mongo --eval "db.adminCommand('ping')"

# 重启MongoDB
# macOS
brew services restart mongodb-community

# Linux
sudo systemctl restart mongod
```

### 3. Redis连接失败
```bash
# 检查Redis状态
redis-cli ping

# 重启Redis
# macOS
brew services restart redis

# Linux
sudo systemctl restart redis
```

### 4. 没有新闻显示
- 等待5分钟左右让系统自动抓取
- 检查AI服务日志是否有错误
- 确认网络连接正常

### 5. WebSocket连接失败
- 检查后端服务是否正常运行
- 确认防火墙没有阻止端口5000
- 查看浏览器控制台错误信息

## 性能优化

### GPU加速（推荐）

如果有NVIDIA GPU：

```bash
# 安装NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# 使用GPU版docker-compose
docker-compose up -d
```

### 调整模型

根据硬件配置选择合适的模型：

- **8GB+ RAM**: `qwen2:7b` 或 `llama3`
- **16GB+ RAM**: `qwen2:14b`
- **4GB RAM**: `qwen2:1.5b`（速度快但准确度低）

## 生产部署

### 1. 使用环境变量

```bash
# 生产环境配置
NODE_ENV=production
MONGODB_URI=mongodb://your-production-db:27017/news-brief
REDIS_URL=redis://your-production-redis:6379
```

### 2. 使用Nginx反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
    }

    location /api {
        proxy_pass http://localhost:5000;
    }

    location /socket.io {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }
}
```

## 技术支持

如果遇到问题：
1. 查看各服务的日志文件
2. 确认所有依赖服务正常运行
3. 检查端口是否被占用
4. 参考项目README.md

## 下一步

- 自定义新闻源
- 调整AI提示词优化摘要质量
- 添加更多分类
- 集成用户登录和个性化订阅
