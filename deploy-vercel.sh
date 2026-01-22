#!/bin/bash

echo "======================================"
echo "实时新闻简报平台 - Vercel 部署脚本"
echo "======================================"
echo ""

# 检查是否安装了vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "📦 安装 Vercel CLI..."
    npm install -g vercel
fi

echo "🔐 登录 Vercel..."
vercel login

echo ""
echo "📝 部署前端..."
cd frontend
vercel --prod

echo ""
echo "📝 部署后端..."
cd ../backend
vercel --prod

echo ""
echo "======================================"
echo "✅ 部署完成！"
echo "======================================"
echo ""
echo "⚠️  重要提示："
echo ""
echo "1. 需要配置云数据库："
echo "   - MongoDB Atlas: https://www.mongodb.com/cloud/atlas"
echo "   - Upstash Redis: https://upstash.com/"
echo ""
echo "2. 在 Vercel 项目设置中添加环境变量"
echo ""
echo "3. 前端环境变量："
echo "   - REACT_APP_API_URL=后端URL"
echo "   - REACT_APP_WS_URL=后端URL"
echo ""
echo "4. 后端环境变量："
echo "   - MONGODB_URI=你的MongoDB URL"
echo "   - REDIS_URL=你的Redis URL"
echo "   - FRONTEND_URL=前端URL"
echo ""
echo "5. AI服务环境变量："
echo "   - USE_CLOUD_AI=true"
echo "   - AI_PROVIDER=openai"
echo "   - OPENAI_API_KEY=你的密钥"
echo ""
