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
      // 核心科技领域
      'ai_technology',         // AI技术
      'robotics',              // 机器人
      'ai_programming',        // AI编码与智能体
      'semiconductors',        // 芯片半导体
      'automotive',            // 汽车
      'consumer_electronics',  // 消费电子
      'podcasts',              // 播客推荐
      'finance_investment',    // 投资财经
      
      // 主流新闻分类
      'business_tech',         // 商业科技
      'politics_world',        // 政治国际
      'economy_policy',        // 经济政策
      'health_medical',        // 健康医疗
      'energy_environment',    // 能源环境
      'entertainment_sports',  // 娱乐体育
      
      // 兴趣领域
      'anime',                 // 动漫二次元
      'one_piece',             // OP（海贼王）
      'tcg',                   // TCG集换式卡牌（OPCG/PTCG/游戏王等）
      
      // 综合
      'general',               // 综合
      
      // 兼容旧数据
      'opcg'                   // 旧OPCG分类（将迁移到tcg）
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

// 创建索引
briefSchema.index({ created_at: -1 });
briefSchema.index({ category: 1 });
briefSchema.index({ is_pushed: 1 });

module.exports = mongoose.model('Brief', briefSchema);
