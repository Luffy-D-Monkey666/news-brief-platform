#!/bin/bash

echo "======================================"
echo "实时新闻简报平台 - 本地开发环境启动"
echo "======================================"

# 检查Ollama是否安装
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama未安装，请先运行: bash setup-ollama.sh"
    exit 1
fi

# 启动Ollama服务（后台）
echo "🚀 启动Ollama服务..."
ollama serve &
OLLAMA_PID=$!
sleep 3

# 检查MongoDB
if ! pgrep -x "mongod" > /dev/null; then
    echo "❌ MongoDB未运行，请启动MongoDB服务"
    echo "   macOS: brew services start mongodb-community"
    echo "   Linux: sudo systemctl start mongod"
    kill $OLLAMA_PID
    exit 1
fi

# 检查Redis
if ! pgrep -x "redis-server" > /dev/null; then
    echo "❌ Redis未运行，请启动Redis服务"
    echo "   macOS: brew services start redis"
    echo "   Linux: sudo systemctl start redis"
    kill $OLLAMA_PID
    exit 1
fi

echo "✅ 所有依赖服务已就绪"
echo ""

# 复制环境变量文件
echo "📝 配置环境变量..."
[ ! -f backend/.env ] && cp backend/.env.example backend/.env
[ ! -f ai-service/.env ] && cp ai-service/.env.example ai-service/.env
[ ! -f frontend/.env ] && cp frontend/.env.example frontend/.env

# 启动AI服务
echo "🤖 启动AI服务..."
cd ai-service
pip install -r requirements.txt > /dev/null 2>&1
python src/main.py &
AI_PID=$!
cd ..

sleep 5

# 启动后端服务
echo "⚙️  启动后端服务..."
cd backend
npm install > /dev/null 2>&1
npm run dev &
BACKEND_PID=$!
cd ..

sleep 5

# 启动前端服务
echo "🎨 启动前端服务..."
cd frontend
npm install > /dev/null 2>&1
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "======================================"
echo "✅ 所有服务启动完成！"
echo "======================================"
echo "📱 前端: http://localhost:3000"
echo "🔧 后端API: http://localhost:5000"
echo "🤖 AI服务: http://localhost:8000"
echo "======================================"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo '停止所有服务...'; kill $OLLAMA_PID $AI_PID $BACKEND_PID $FRONTEND_PID; exit" INT
wait
