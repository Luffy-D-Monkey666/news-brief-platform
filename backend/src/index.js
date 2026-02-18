require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const http = require('http');
const { Server } = require('socket.io');

const briefRoutes = require('./routes/briefs');
const topicRoutes = require('./routes/topics');
const ttsRoutes = require('./routes/tts');
const WebSocketService = require('./services/websocketService');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    methods: ['GET', 'POST']
  }
});

// 环境变量 - 确保正确读取
const PORT = process.env.PORT || 5000;
const MONGODB_URI = process.env.MONGODB_URI;
const REDIS_URL = process.env.REDIS_URL;

// 调试信息：打印环境变量
console.log('=== 环境变量检查 ===');
console.log('MONGODB_URI:', MONGODB_URI);
console.log('MONGODB_URI type:', typeof MONGODB_URI);
console.log('MONGODB_URI length:', MONGODB_URI ? MONGODB_URI.length : 0);
console.log('REDIS_URL:', REDIS_URL);
console.log('==================');

// 检查必需的环境变量
if (!MONGODB_URI) {
  console.error('错误: MONGODB_URI 环境变量未设置');
  process.exit(1);
}
if (!REDIS_URL) {
  console.error('错误: REDIS_URL 环境变量未设置');
  process.exit(1);
}

// 中间件
app.use(helmet());
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 健康检查
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    mongodb: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected'
  });
});

// 将原生MongoDB连接挂载到app.locals供路由使用
mongoose.connection.once('open', () => {
  app.locals.db = mongoose.connection.db;
});

// API路由
app.use('/api/briefs', briefRoutes);
app.use('/api/topics', topicRoutes);
app.use('/api/tts', ttsRoutes);

// 404处理
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: 'API路由不存在'
  });
});

// 错误处理
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    message: '服务器内部错误'
  });
});

// WebSocket服务
const wsService = new WebSocketService(io);

// 连接MongoDB
console.log('=== 准备连接MongoDB ===');
console.log('连接字符串:', MONGODB_URI);
console.log('连接字符串开头:', MONGODB_URI.substring(0, 20));
console.log('=====================');

mongoose.connect(MONGODB_URI, {
  serverSelectionTimeoutMS: 10000,
  socketTimeoutMS: 45000,
  family: 4  // 强制使用 IPv4，避免 IPv6 DNS 问题
})
  .then(() => {
    console.log('✅ MongoDB连接成功');
  })
  .catch((err) => {
    console.error('❌ MongoDB连接失败:', err);
    console.error('尝试连接的URI:', MONGODB_URI);
    process.exit(1);
  });

// 初始化WebSocket服务
wsService.initialize(REDIS_URL)
  .then(() => {
    console.log('✅ WebSocket服务初始化成功');
  })
  .catch((err) => {
    console.error('❌ WebSocket服务初始化失败:', err);
  });

// WebSocket连接处理
io.on('connection', (socket) => {
  wsService.handleConnection(socket);
});

// 启动服务器
server.listen(PORT, () => {
  console.log('='.repeat(50));
  console.log(`🚀 新闻简报后端服务已启动`);
  console.log(`📡 HTTP服务: http://localhost:${PORT}`);
  console.log(`🔌 WebSocket服务: ws://localhost:${PORT}`);
  console.log(`🗄️  MongoDB: ${MONGODB_URI}`);
  console.log(`📮 Redis: ${REDIS_URL}`);
  console.log('='.repeat(50));
});

// 优雅关闭
process.on('SIGTERM', async () => {
  console.log('收到SIGTERM信号，开始优雅关闭...');
  await wsService.close();
  await mongoose.connection.close();
  server.close(() => {
    console.log('服务已关闭');
    process.exit(0);
  });
});
