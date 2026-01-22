const redis = require('redis');

class WebSocketService {
  constructor(io) {
    this.io = io;
    this.redisClient = null;
    this.redisSubscriber = null;
  }

  async initialize(redisUrl) {
    // 创建Redis客户端
    this.redisClient = redis.createClient({ url: redisUrl });
    this.redisSubscriber = this.redisClient.duplicate();

    await this.redisClient.connect();
    await this.redisSubscriber.connect();

    // 订阅Redis频道
    await this.redisSubscriber.subscribe('news:new', (message) => {
      try {
        const brief = JSON.parse(message);
        this.broadcastBrief(brief);
      } catch (error) {
        console.error('处理Redis消息失败:', error);
      }
    });

    console.log('WebSocket服务已初始化，已订阅Redis频道');
  }

  broadcastBrief(brief) {
    // 广播到所有连接的客户端
    this.io.emit('news:update', brief);

    // 广播到特定分类房间
    this.io.to(`category:${brief.category}`).emit('category:update', brief);

    console.log(`广播简报: [${brief.category}] ${brief.title}`);
  }

  handleConnection(socket) {
    console.log('客户端连接:', socket.id);

    // 客户端订阅特定分类
    socket.on('subscribe:category', (category) => {
      socket.join(`category:${category}`);
      console.log(`客户端 ${socket.id} 订阅分类: ${category}`);
    });

    // 客户端取消订阅
    socket.on('unsubscribe:category', (category) => {
      socket.leave(`category:${category}`);
      console.log(`客户端 ${socket.id} 取消订阅分类: ${category}`);
    });

    // 客户端断开连接
    socket.on('disconnect', () => {
      console.log('客户端断开:', socket.id);
    });

    // 发送欢迎消息
    socket.emit('connected', {
      message: '已连接到新闻简报服务',
      socketId: socket.id
    });
  }

  async close() {
    if (this.redisClient) {
      await this.redisClient.quit();
    }
    if (this.redisSubscriber) {
      await this.redisSubscriber.quit();
    }
  }
}

module.exports = WebSocketService;
