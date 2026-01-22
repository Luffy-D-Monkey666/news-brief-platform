require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const http = require('http');
const { Server } = require('socket.io');

const briefRoutes = require('./routes/briefs');
const WebSocketService = require('./services/websocketService');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    methods: ['GET', 'POST']
  }
});

// 环境变量
const PORT = process.env.PORT || 5000;
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/news-brief';
const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';

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

// API路由
app.use('/api/briefs', briefRoutes);

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
mongoose.connect(MONGODB_URI)
  .then(() => {
    console.log('✅ MongoDB连接成功');
  })
  .catch((err) => {
    console.error('❌ MongoDB连接失败:', err);
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
