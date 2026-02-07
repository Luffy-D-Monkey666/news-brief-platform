const mongoose = require('mongoose');

const briefSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  summary: {
    type: String,
    required: true
  },
  category: {
    type: String,
    required: true,
    enum: [
      'ai_technology',         // AI技术（机器学习、大语言模型、AI应用）
      'robotics',              // 机器人（工业/服务/人形/移动机器人、自动驾驶、DMS、智能座舱）
      'ai_coding_agent',       // AI编码与智能体（AI Coding + AI Agent）
      'anime_otaku',           // 动漫二次元（日本+欧洲动画漫画）
      'semiconductors',        // 芯片半导体（芯片设计、制造、设备、材料）
      'opcg',                  // OPCG卡牌游戏（One Piece Card Game）
      'automotive',            // 汽车（电动车/燃油车/混动车、充电桩、电池、新车、销量）
      'consumer_electronics',  // 消费电子（手机、手表、眼镜、相机、无人机等）
      'one_piece',             // ONE PIECE（海贼王动漫周边）
      'podcasts',              // 播客推荐（优质播客节目内容推荐）
      'finance_investment',    // 投资财经
      'business_tech',         // 商业科技
      'politics_world',        // 政治国际
      'economy_policy',        // 经济政策
      'health_medical',        // 健康医疗
      'energy_environment',    // 能源环境
      'entertainment_sports',  // 娱乐体育
      'general'               // 综合
    ]
  },
  source: {
    type: String,
    required: true
  },
  source_url: {
    type: String
  },
  link: {
    type: String,
    required: true
  },
  image: {
    type: String,
    default: null
  },
  video: {
    type: String,
    default: null
  },
  published: {
    type: Date,
    default: Date.now
  },
  created_at: {
    type: Date,
    default: Date.now
  },
  is_pushed: {
    type: Boolean,
    default: false
  },
  pushed_at: {
    type: Date
  }
});

// 创建索引（优化查询性能）
briefSchema.index({ created_at: -1 });  // 时间倒序查询
briefSchema.index({ category: 1, created_at: -1 });  // 复合索引：按分类+时间查询（最常用）
briefSchema.index({ is_pushed: 1 });

module.exports = mongoose.model('Brief', briefSchema);
