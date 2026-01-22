#!/bin/bash

echo "======================================"
echo "实时新闻简报平台 - Railway 一键部署"
echo "======================================"
echo ""

# 检查是否安装了railway CLI
if ! command -v railway &> /dev/null; then
    echo "📦 安装 Railway CLI..."
    npm install -g @railway/cli
fi

# 检查是否已登录
echo "🔐 登录 Railway..."
railway login

# 创建新项目
echo "🚀 创建新项目..."
railway init

# 添加MongoDB
echo "🗄️ 添加 MongoDB..."
railway add --plugin mongodb

# 添加Redis
echo "📮 添加 Redis..."
railway add --plugin redis

echo ""
echo "======================================"
echo "✅ 基础设置完成！"
echo "======================================"
echo ""
echo "接下来需要手动配置："
echo ""
echo "1. 在 Railway 控制台添加以下环境变量："
echo ""
echo "   【AI Service】"
echo "   - USE_CLOUD_AI=true"
echo "   - AI_PROVIDER=openai"
echo "   - OPENAI_API_KEY=你的OpenAI密钥"
echo "   - MONGODB_URI=\${{MongoDB.MONGO_URL}}"
echo "   - REDIS_URL=\${{Redis.REDIS_URL}}"
echo ""
echo "   【Backend】"
echo "   - MONGODB_URI=\${{MongoDB.MONGO_URL}}"
echo "   - REDIS_URL=\${{Redis.REDIS_URL}}"
echo "   - FRONTEND_URL=前端URL（部署后获得）"
echo ""
echo "   【Frontend】"
echo "   - REACT_APP_API_URL=后端URL（部署后获得）"
echo "   - REACT_APP_WS_URL=后端URL（部署后获得）"
echo ""
echo "2. 推送代码到GitHub"
echo "3. 在Railway控制台连接GitHub仓库"
echo "4. 部署完成后，访问提供的URL"
echo ""
echo "详细教程: https://docs.railway.app/deploy/deployments"
echo ""
